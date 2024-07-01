import argparse
import asyncio

from models import Series
from requests_fetch_strategy import RequestsStrategy, AIOHttpStrategy
from texttable import Texttable
from colorama import Back, Style, Fore
import settings
from datetime import datetime

from web import delta_days, get_aired_data, reverse_date, search_series


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", help="Search query")
    args = parser.parse_args()
    query = args.query

    print_alert_message()

    print(f"Searching for {query}...")
    series = asyncio.run(fetch_series(query))

    print(f"Found {len(series)} series. Fetching data...")
    extra = asyncio.run(fetch_aired_data(series))

    print(stats(series))
    print(render_ascii_table(series, extra))


def print_alert_message():
    expiration_datetime = datetime.fromtimestamp(
        int(settings.JWT_EXPIRATION_DATETIME)
    ).astimezone()
    now_with_tz = datetime.now().astimezone()
    time_zone = now_with_tz.tzinfo
    days = (now_with_tz - expiration_datetime).days

    if days <= 0:
        print(
            f"{Fore.YELLOW}"
            f"You can use this app for {abs(days)} more day(s).\n"
            f"On {expiration_datetime.strftime('%d-%m-%Y %H:%M:%S')} ({time_zone}) the access token will expire, preventing you from using the application! "
            f"Do not expect things to work after this date!"
            f"{Style.RESET_ALL}"
        )
    else:
        print(
            f"{Fore.RED}"
            "It appears that the access token has expired!"
            f"{Style.RESET_ALL}"
        )


async def fetch_series(query: str) -> list[Series]:
    fetch_strategy = RequestsStrategy()
    return await search_series(query, fetch_strategy=fetch_strategy)


async def fetch_aired_data(series: list[Series]) -> dict[str, dict[str, str]]:
    fetch_strategy = AIOHttpStrategy()
    extra: dict[str, dict[str, str]] = dict()
    tasks = []
    for s in series:
        tasks.append(
            (s.tvdb_id, asyncio.create_task(get_aired_data(s, fetch_strategy=fetch_strategy)))
        )
    for tvdb_id, t in tasks:
        aired_data = await t
        extra[tvdb_id] = aired_data
    return extra


def stats(series: list[Series]) -> str:
    continuing, upcoming, ended = 0, 0, 0
    for s in series:
        if s.status == "Continuing":
            continuing += 1
        elif s.status == "Ended":
            ended += 1
        elif s.status == "Upcoming":
            upcoming += 1

    return (
        f"Total results: {Fore.BLACK + Back.WHITE + str(len(series)).ljust(3) + Style.RESET_ALL} "
        f"Continuing: {Fore.BLACK + Back.GREEN + str(continuing).ljust(3) + Style.RESET_ALL} "
        f"Upcoming: {Fore.BLACK + Back.BLUE + str(upcoming).ljust(3) + Style.RESET_ALL} "
        f"Ended: {Fore.BLACK + Back.RED + str(ended).ljust(3) + Style.RESET_ALL}"
    )


def get_colored_status(s: Series) -> str:
    background = ""
    if s.status == "Continuing":
        background = Back.GREEN
    elif s.status == "Ended":
        background = Back.RED
    elif s.status == "Upcoming":
        background = Back.BLUE
    return f"{Fore.BLACK}{background}{s.status}{Style.RESET_ALL}"


def render_next_aired(s: Series, extra: dict[str, dict[str, str | None]]) -> str:
    next_aired = extra[s.tvdb_id]["next_aired"]
    if next_aired:
        reversed_date = reverse_date(next_aired)
        dd = delta_days(reversed_date)
        if dd < 0:
            return f"watch in {abs(dd)} days ({reversed_date})"
        else:
            return f"{reversed_date}"
    else:
        return f"No upcoming episodes {'yet' if s.status in ['Continuing', 'Upcoming'] else ''}"


def render_last_aired(s: Series, extra: dict[str, dict[str, str]]) -> str:
    last_aired = extra[s.tvdb_id]["last_aired"]
    if last_aired:
        return reverse_date(last_aired)
    else:
        return "N/A"


def render_ascii_table(series: list[Series], extra: dict[str, dict[str, str]]) -> str:
    table = Texttable(max_width=0)
    table.add_rows(
        [
            ["Title", "Next Episode", "Last Episode", "Status"],
            *[
                [
                    s.name,
                    render_next_aired(s, extra),
                    render_last_aired(s, extra),
                    get_colored_status(s),
                ]
                for s in series
            ],
        ]
    )
    return table.draw()


if __name__ == "__main__":
    main()

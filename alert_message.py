from js import document
from datetime import datetime, timezone
import settings

expiration_datetime = datetime.fromtimestamp(
    int(settings.JWT_EXPIRATION_DATETIME)
).astimezone()
now_with_tz = datetime.now().astimezone()
time_zone = now_with_tz.tzinfo
days = (now_with_tz - expiration_datetime).days
if days <= 0:
    document.getElementById("expiration-days").textContent = f"{abs(days)}"
    document.getElementById(
        "expiration-datetime"
    ).textContent = f"{expiration_datetime.strftime('%d-%m-%Y %H:%M:%S')}"
    document.getElementById("expiration-tz").textContent = f"{time_zone}"
else:
    document.getElementById("token-expired").classList.remove("d-none")
    document.getElementById("token-not-expired").classList.add("d-none")


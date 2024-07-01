from dataclasses import dataclass


@dataclass
class Series:
    id: str
    name: str
    status: str
    tvdb_id: str
    thumbnail: str

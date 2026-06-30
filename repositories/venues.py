import api
from models.venue import Venue, VenueSummary


def all() -> list[VenueSummary]:
    return [VenueSummary.from_dict(v) for v in api.request("venues")["data"]]


def get(venue_ref: int) -> Venue:
    return Venue.from_dict(api.request(f"venues/{venue_ref}")["data"])

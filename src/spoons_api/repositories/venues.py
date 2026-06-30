import datetime

import spoons_api.api as api
from spoons_api.models.venue import Venue, VenueSummary


def all(max_age: datetime.timedelta | None = None) -> list[VenueSummary]:
    return [
        VenueSummary.from_dict(v)
        for v in api.request("venues", max_age=max_age)["data"]
    ]


def get(venue_summary: VenueSummary, max_age: datetime.timedelta | None = None) -> Venue:
    return Venue.from_dict(api.request(f"venues/{venue_summary.venue_ref}", max_age=max_age)["data"])

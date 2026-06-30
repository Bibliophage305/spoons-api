from datetime import datetime

import spoons_api.api as api
from spoons_api.models.venue import Venue
from spoons_api.models.menu import Menu, MenuSummary


def all(
    venue: Venue,
    max_age: datetime.timedelta | None = None,
) -> list[MenuSummary]:
    return [
        MenuSummary.from_dict(m)
        for m in api.request(
            f"{venue.franchise}/venues/{venue.venue_ref}/sales-areas/{venue.sales_areas[0].id}/menus",
            max_age=max_age,
        )["data"]
    ]


def get(
    venue: Venue,
    menu_summary: MenuSummary,
    max_age: datetime.timedelta | None = None,
) -> Menu:
    return Menu.from_dict(
        api.request(
            f"{venue.franchise}/venues/{venue.venue_ref}/sales-areas/{venue.sales_areas[0].id}/menus/{menu_summary.id}",
            max_age=max_age,
        )["data"]
    )

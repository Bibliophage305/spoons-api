from datetime import datetime

import spoons_api.api as api
from spoons_api.models.menu import Menu, MenuSummary


def all(
    franchise: str,
    venue_ref: int,
    sales_area_id: int,
    max_age: datetime.timedelta | None = None,
) -> list[MenuSummary]:
    return [
        MenuSummary.from_dict(m)
        for m in api.request(
            f"{franchise}/venues/{venue_ref}/sales-areas/{sales_area_id}/menus",
            max_age=max_age,
        )["data"]
    ]


def get(
    franchise: str,
    venue_ref: int,
    sales_area_id: int,
    menu_id: int,
    max_age: datetime.timedelta | None = None,
) -> Menu:
    return Menu.from_dict(
        api.request(
            f"{franchise}/venues/{venue_ref}/sales-areas/{sales_area_id}/menus/{menu_id}",
            max_age=max_age,
        )["data"]
    )

import spoons_api.api as api
from spoons_api.models.menu import Menu, MenuSummary


def all(franchise: str, venue_ref: int, sales_area_id: int) -> list[MenuSummary]:
    return [
        MenuSummary.from_dict(m)
        for m in api.request(
            f"{franchise}/venues/{venue_ref}/sales-areas/{sales_area_id}/menus"
        )["data"]
    ]


def get(franchise: str, venue_ref: int, sales_area_id: int, menu_id: int) -> Menu:
    return Menu.from_dict(
        api.request(
            f"{franchise}/venues/{venue_ref}/sales-areas/{sales_area_id}/menus/{menu_id}"
        )["data"]
    )

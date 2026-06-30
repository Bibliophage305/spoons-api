from spoons_api.repositories.venues import get as get_venue
from spoons_api.repositories.menus import all as get_all_menus, get as get_menu
from spoons_api.models.venue import Venue, VenueSummary
from spoons_api.models.menu import Menu, MenuSummary


def test_venue_summary_round_trip(venue_summaries):
    for summary in venue_summaries:
        assert summary == VenueSummary.from_dict(summary.to_dict())


def test_venue_round_trip(venue_summaries):
    for summary in venue_summaries:
        venue = get_venue(summary.venue_ref)
        assert venue == Venue.from_dict(venue.to_dict())


def test_menu_round_trip(venue_summaries):
    for summary in venue_summaries:
        venue = get_venue(summary.venue_ref)
        sales_area_id = venue.sales_areas[0].id
        for menu_summary in get_all_menus(
            venue.franchise, venue.venue_ref, sales_area_id
        ):
            assert menu_summary == MenuSummary.from_dict(menu_summary.to_dict())
            menu = get_menu(
                venue.franchise, venue.venue_ref, sales_area_id, menu_summary.id
            )
            assert menu == Menu.from_dict(menu.to_dict())

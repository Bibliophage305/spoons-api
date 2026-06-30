from repositories.venues import all as get_all_venues, get as get_venue
from repositories.menus import all as get_all_menus, get as get_menu
from models.venue import Venue, VenueSummary
from models.menu import Menu, MenuSummary


def main():
    for venue_summary in get_all_venues():
        assert venue_summary == VenueSummary.from_dict(venue_summary.to_dict())
        venue = get_venue(venue_summary.venue_ref)
        assert venue == Venue.from_dict(venue.to_dict())
        menu_summaries = get_all_menus(
            venue.franchise, venue.venue_ref, venue.sales_areas[0].id
        )
        for menu_summary in menu_summaries:
            assert menu_summary == MenuSummary.from_dict(menu_summary.to_dict())
            menu = get_menu(
                venue.franchise,
                venue.venue_ref,
                venue.sales_areas[0].id,
                menu_summary.id,
            )
            assert menu == Menu.from_dict(menu.to_dict())


if __name__ == "__main__":
    main()

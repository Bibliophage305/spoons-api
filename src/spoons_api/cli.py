import questionary

from spoons_api.drinks import extract_drinks
from spoons_api.models.venue import VenueSummary
from spoons_api.repositories.menus import all as get_all_menus, get as get_menu
from spoons_api.repositories.venues import all as get_all_venues, get as get_venue


def venue_to_name_and_address(venue: VenueSummary) -> str:
    return f"{venue.name}, {venue.address.town}, {venue.address.county}, {venue.address.postcode}, {venue.address.country.name}"


def choose_venue(venue_summaries: list[VenueSummary]) -> VenueSummary:
    choice = questionary.autocomplete(
        "Choose venue",
        choices=[venue_to_name_and_address(venue) for venue in venue_summaries],
    ).ask()
    return next(
        venue for venue in venue_summaries if venue_to_name_and_address(venue) == choice
    )


def main():
    questionary.print("Welcome to the Spoons API CLI!", style="bold fg:green")
    questionary.print(
        "We're going to calculate the cheapest way to get drunk at a Wetherspoons venue.",
        style="bold fg:green",
    )

    venue_summary = choose_venue(get_all_venues())
    venue = get_venue(venue_summary)

    menu_summaries = get_all_menus(venue)
    menus = [get_menu(venue, menu_summary) for menu_summary in menu_summaries]

    drinks = extract_drinks(menus)
    for drink in drinks:
        print(drink)


if __name__ == "__main__":
    main()

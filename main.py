import questionary

import re

from spoons_api.models.venue import VenueSummary

from spoons_api.repositories.venues import all as get_all_venues, get as get_venue
from spoons_api.repositories.menus import all as get_all_menus, get as get_menu


def venue_to_name_and_address(venue: VenueSummary) -> str:
    return f"{venue.name}, {venue.address.town}, {venue.address.county}, {venue.address.postcode}, {venue.address.country.name}"


def main():
    questionary.print("Welcome to the Spoons API CLI!", style="bold fg:green")
    questionary.print(
        "We're going to calculate the cheapest way to get drunk at a Wetherspoons venue.",
        style="bold fg:green",
    )
    venue_summaries = get_all_venues()
    venue_name_and_address = questionary.autocomplete(
        "Choose venue",
        choices=[venue_to_name_and_address(venue) for venue in venue_summaries],
    ).ask()
    venue_summary = next(
        venue
        for venue in venue_summaries
        if venue_to_name_and_address(venue) == venue_name_and_address
    )
    venue = get_venue(venue_summary)
    menu_summaries = get_all_menus(venue)
    menus = [get_menu(venue, menu_summary) for menu_summary in menu_summaries]
    drinks = []
    for menu in menus:
        for category in menu.categories:
            for item_group in category.item_groups:
                for item in item_group.items:
                    if item.item_type == "product":
                        abv = item.abv
                        if item.name == "Hugo Spritz":
                            abv = 100 * (0.413 * 25 + 0.11 * 125) / 150
                        elif item.name == "Mango & Passionfruit Spritz":
                            abv = 100 * (0.35 * 25 + 0.11 * 125) / 150
                        elif item.name == "Classic Aperol Spritz":
                            abv = 100 * (0.11 * 50 + 0.11 * 125) / 175
                        elif item.name == "Peach Blush Spritz":
                            abv = 100 * (0.18 * 25 + 0.115 * 125) / 150
                        elif item.name == "Limoncello Spritz":
                            abv = 100 * (0.3 * 50 + 0.11 * 125) / 175
                        if abv == 0:
                            continue
                        for option in item.options.portion.options:
                            volume_match = re.search(
                                r"\d+\.?\d*(?=ml)", option.value.name.lower()
                            )
                            description_volume_match = re.search(
                                r"\d+\.?\d*(?=ml)", item.description.lower()
                            )
                            if volume_match:
                                volume = int(volume_match.group(0))
                            elif item.name in ("Hugo Spritz", "Mango & Passionfruit Spritz", "Peach Blush Spritz"):
                                volume = 150
                            elif item.name in ("Classic Aperol Spritz", "Limoncello Spritz"):
                                volume = 175
                            elif "half pint" in option.value.name.lower():
                                volume = 284
                            elif "half" in option.value.name.lower():
                                volume = 284
                            elif "third pint" in option.value.name.lower():
                                volume = 189
                            elif "third" in option.value.name.lower():
                                volume = 189
                            elif "pint" in option.value.name.lower():
                                volume = 568
                            elif "single" in option.value.name.lower():
                                volume = 25
                            elif "double" in option.value.name.lower():
                                volume = 50
                            elif (
                                any(
                                    keyword in option.value.name.lower()
                                    for keyword in [
                                        "standard",
                                        "can",
                                        "bottle",
                                        "glass",
                                        "pitcher",
                                    ]
                                )
                                and description_volume_match
                            ):
                                volume = int(description_volume_match.group(0))
                            elif units_match := re.search(
                                r"\d+\.?\d*(?= unit)", item.description.lower()
                            ):
                                units = float(units_match.group(0))
                                volume_estimate = units * 1000 / abv
                                known_volumes = [
                                    25,
                                    50,
                                    125,
                                    175,
                                    250,
                                    284,
                                    330,
                                    440,
                                    500,
                                    568,
                                    750,
                                    1000,
                                ]
                                volume = min(
                                    known_volumes,
                                    key=lambda x: abs(x - volume_estimate),
                                )
                            elif item_group.name.lower() == "classic cocktails":
                                volume = 125
                            elif category.name.lower() == "includes a drink" and item_group.name.lower() == "spritz cocktails":
                                volume = 125
                            else:
                                print("couldn't find volume")
                                print(f"{category.name=}")
                                print(f"{item_group.name=}")
                                print(f"{item.name=}")
                                print(f"{option.value.name=}")
                                print(
                                    f"Maybe it's in this description:\n{item.description}"
                                )
                                for k, v in item.to_dict().items():
                                    print(k, v)
                                input()
                                continue
                            drinks.append(
                                (
                                    (1000 * option.value.price.value) / (abv * volume),
                                    item.name,
                                    option.value.name,
                                    abv,
                                    option.value.price.value,
                                    option.value.price.currency,
                                    volume,
                                )
                            )
                            if item.options.linked:
                                for linked_option in item.options.linked:
                                    option_name_tokens = linked_option.name.lower().split()
                                    multiplier = int(option_name_tokens[1])
                                    multiple_price = float(option_name_tokens[-1][1:])
                                    drinks.append(
                                        (
                                            (1000 * multiple_price) / (abv * volume * multiplier),
                                            item.name,
                                            linked_option.name,
                                            abv,
                                            multiple_price,
                                            option.value.price.currency,
                                            volume * multiplier,
                                        )
                                    )
    drinks = sorted(set(drinks))
    for drink in drinks:
        currency_symbol = {
            "EUR": "€",
            "GBP": "£",
        }.get(drink[5])
        print(
            f"{drink[1]} - {drink[2]} - {drink[3]}% - {currency_symbol}{drink[4]} - {drink[6]}ml - {currency_symbol}{drink[0]:.2f} per unit of alcohol"
        )


if __name__ == "__main__":
    main()

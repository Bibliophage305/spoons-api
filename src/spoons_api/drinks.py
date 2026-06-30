"""Extract priced, drinkable items from a menu and rank by cost per unit of alcohol."""

import re
from dataclasses import dataclass

from spoons_api.models.menu import Menu, ProductItem

# Wetherspoons spritzes don't expose a usable ABV directly — they're a mix of
# two components at different volumes. Worked out by hand from the menu
# descriptions; (component % ABV * component ml) summed, divided by total ml.
SPRITZ_ABV_OVERRIDES: dict[str, float] = {
    "Hugo Spritz": 100 * (0.413 * 25 + 0.11 * 125) / 150,
    "Mango & Passionfruit Spritz": 100 * (0.35 * 25 + 0.11 * 125) / 150,
    "Classic Aperol Spritz": 100 * (0.11 * 50 + 0.11 * 125) / 175,
    "Peach Blush Spritz": 100 * (0.18 * 25 + 0.115 * 125) / 150,
    "Limoncello Spritz": 100 * (0.3 * 50 + 0.11 * 125) / 175,
}

# Spritzes where the serve size isn't stated as "Xml" anywhere and has to be
# inferred from which spritz it is.
SPRITZ_VOLUME_OVERRIDES: dict[str, int] = {
    "Hugo Spritz": 150,
    "Mango & Passionfruit Spritz": 150,
    "Peach Blush Spritz": 150,
    "Classic Aperol Spritz": 175,
    "Limoncello Spritz": 175,
}

# Standard serve sizes (ml) keyed by a keyword found in the option name.
SERVE_SIZE_KEYWORDS: dict[str, int] = {
    "half pint": 284,
    "half": 284,
    "third pint": 189,
    "third": 189,
    "pint": 568,
    "single": 25,
    "double": 50,
}

# When a volume can't be read from the option name but the description gives
# units of alcohol, the implied volume is rounded to the nearest of these.
KNOWN_BOTTLE_AND_GLASS_VOLUMES_ML = [
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

VOLUME_FROM_DESCRIPTION_KEYWORDS = ("standard", "can", "bottle", "glass", "pitcher")

CURRENCY_SYMBOLS = {"EUR": "€", "GBP": "£"}


@dataclass(frozen=True, order=True)
class Drink:
    cost_per_unit: float
    item_name: str
    option_name: str
    abv: float
    price: float
    currency: str
    volume_ml: int

    @property
    def currency_symbol(self) -> str:
        return CURRENCY_SYMBOLS.get(self.currency, self.currency)

    def __str__(self) -> str:
        return (
            f"{self.item_name} - {self.option_name} - {self.abv}% - "
            f"{self.currency_symbol}{self.price} - {self.volume_ml}ml - "
            f"{self.currency_symbol}{self.cost_per_unit:.2f} per unit of alcohol"
        )


class VolumeNotFoundError(Exception):
    """Raised when an option's serving volume can't be determined."""


def _extract_ml(text: str) -> int | None:
    match = re.search(r"\d+\.?\d*(?=ml)", text.lower())
    return int(match.group(0)) if match else None


def _extract_units(description: str) -> float | None:
    match = re.search(r"\d+\.?\d*(?= unit)", description.lower())
    return float(match.group(0)) if match else None


def resolve_abv(item: ProductItem) -> float:
    """Return the item's ABV, applying spritz overrides where needed."""
    return SPRITZ_ABV_OVERRIDES.get(item.name, item.abv)


def resolve_volume_ml(
    item: ProductItem,
    category_name: str,
    item_group_name: str,
    option_name: str,
    abv: float,
) -> int:
    """
    Determine the serving volume in ml for a given portion option.

    Tries, in order: an explicit "Xml" in the option name, a known spritz
    override, a recognised serve-size keyword (pint/half/double/etc), an
    "Xml" in the item description, an implied volume from stated alcohol
    units, then a couple of menu-section-specific fallbacks.
    """
    option_name_lower = option_name.lower()

    if volume := _extract_ml(option_name):
        return volume

    if item.name in SPRITZ_VOLUME_OVERRIDES:
        return SPRITZ_VOLUME_OVERRIDES[item.name]

    for keyword, volume in SERVE_SIZE_KEYWORDS.items():
        if keyword in option_name_lower:
            return volume

    if any(
        keyword in option_name_lower for keyword in VOLUME_FROM_DESCRIPTION_KEYWORDS
    ):
        if volume := _extract_ml(item.description):
            return volume

    if (units := _extract_units(item.description)) is not None:
        volume_estimate = units * 1000 / abv
        return min(
            KNOWN_BOTTLE_AND_GLASS_VOLUMES_ML, key=lambda v: abs(v - volume_estimate)
        )

    if item_group_name.lower() == "classic cocktails":
        return 125

    if (
        category_name.lower() == "includes a drink"
        and item_group_name.lower() == "spritz cocktails"
    ):
        return 125

    raise VolumeNotFoundError(
        f"Couldn't determine volume for {item.name!r} / {option_name!r}\n"
        f"Description: {item.description}"
    )


def _cost_per_unit(price: float, abv: float, volume_ml: int) -> float:
    return (1000 * price) / (abv * volume_ml)


def _drinks_for_option(
    item: ProductItem, category_name: str, item_group_name: str, abv: float
) -> list[Drink]:
    drinks = []
    for option in item.options.portion.options:
        volume_ml = resolve_volume_ml(
            item, category_name, item_group_name, option.value.name, abv
        )
        price = option.value.price
        drinks.append(
            Drink(
                cost_per_unit=_cost_per_unit(price.value, abv, volume_ml),
                item_name=item.name,
                option_name=option.value.name,
                abv=abv,
                price=price.value,
                currency=price.currency,
                volume_ml=volume_ml,
            )
        )

        for linked in item.options.linked or []:
            # Linked options are phrased like "x3 for £12.00": a multi-buy on
            # the same base drink at a discounted aggregate price.
            tokens = linked.name.lower().split()
            multiplier = int(tokens[1])
            multiple_price = float(tokens[-1][1:])
            drinks.append(
                Drink(
                    cost_per_unit=_cost_per_unit(
                        multiple_price, abv, volume_ml * multiplier
                    ),
                    item_name=item.name,
                    option_name=linked.name,
                    abv=abv,
                    price=multiple_price,
                    currency=price.currency,
                    volume_ml=volume_ml * multiplier,
                )
            )

    return drinks


def extract_drinks(menus: list[Menu], on_unresolved: str = "skip") -> list[Drink]:
    """
    Flatten every alcoholic product item across the given menus into Drinks.

    on_unresolved controls what happens when a volume can't be determined:
    "skip" silently drops the option, "raise" propagates VolumeNotFoundError.
    """
    drinks: set[Drink] = set()

    for menu in menus:
        for category in menu.categories:
            for item_group in category.item_groups:
                for item in item_group.items:
                    if item.item_type != "product":
                        continue

                    abv = resolve_abv(item)
                    if abv == 0:
                        continue

                    try:
                        drinks.update(
                            _drinks_for_option(
                                item, category.name, item_group.name, abv
                            )
                        )
                    except VolumeNotFoundError:
                        if on_unresolved == "raise":
                            raise

    return sorted(drinks)

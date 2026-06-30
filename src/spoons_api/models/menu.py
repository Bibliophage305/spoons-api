from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate

import re


@dataclass_validate
@dataclass
class MenuSummary:
    can_order: bool
    franchise: str
    id: int
    name: str
    sales_area_id: int
    venue_ref: int

    @classmethod
    def _base_kwargs(cls, data: dict) -> dict:
        return dict(
            can_order=data["canOrder"],
            franchise=data["franchise"],
            id=data["id"],
            name=data["name"],
            sales_area_id=data["salesAreaId"],
            venue_ref=data["venueRef"],
        )

    @classmethod
    def from_dict(cls, data: dict) -> "MenuSummary":
        return cls(**cls._base_kwargs(data))

    def to_dict(self) -> dict:
        return {
            "canOrder": self.can_order,
            "franchise": self.franchise,
            "id": self.id,
            "name": self.name,
            "salesAreaId": self.sales_area_id,
            "venueRef": self.venue_ref,
        }


@dataclass_validate
@dataclass
class Item:
    item_type: str

    @classmethod
    def _base_kwargs(cls, data: dict) -> dict:
        return dict(
            item_type=data["itemType"],
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(**cls._base_kwargs(data))

    def to_dict(self) -> dict:
        return {
            "itemType": self.item_type,
        }


@dataclass_validate
@dataclass
class Checkout:
    id: int
    name: str
    menu_id: None
    messages: None

    @classmethod
    def from_dict(cls, data: dict) -> "Checkout":
        return cls(
            id=data["id"],
            name=data["name"],
            menu_id=data["menuId"],
            messages=data["messages"] or None,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "menuId": self.menu_id,
            "messages": self.messages or [],
        }


@dataclass_validate
@dataclass
class ValueChoice:
    choice_id: int
    portion_id: int
    display_record_id: int | None

    @classmethod
    def from_dict(cls, data: dict) -> "ValueChoice":
        return cls(
            choice_id=data["choiceId"],
            portion_id=data["portionId"],
            display_record_id=(
                data["displayRecordId"] if "displayRecordId" in data else None
            ),
        )

    def to_dict(self) -> dict:
        d = {
            "choiceId": self.choice_id,
            "portionId": self.portion_id,
        }
        if self.display_record_id is not None:
            d["displayRecordId"] = self.display_record_id
        return d


@dataclass_validate
@dataclass
class Price:
    initial_value: float
    value: float
    currency: str
    discount: int

    @classmethod
    def from_dict(cls, data: dict) -> "Price":
        return cls(
            initial_value=float(data["initialValue"]),
            value=float(data["value"]),
            currency=data["currency"],
            discount=data["discount"],
        )

    def to_dict(self) -> dict:
        return {
            "initialValue": self.initial_value,
            "value": self.value,
            "currency": self.currency,
            "discount": self.discount,
        }


@dataclass_validate
@dataclass
class Value:
    id: int
    name: str
    description: str | None
    calories: None
    choices: list[ValueChoice]
    price: Price
    checkout: Checkout
    hidden: bool
    is_default: bool

    @classmethod
    def from_dict(cls, data: dict) -> "Value":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            calories=data["calories"],
            choices=[ValueChoice.from_dict(choice) for choice in data["choices"]],
            price=Price.from_dict(data["price"]),
            checkout=Checkout.from_dict(data["checkout"]),
            hidden=data["hidden"],
            is_default=data["isDefault"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "calories": self.calories,
            "choices": [choice.to_dict() for choice in self.choices],
            "price": self.price.to_dict(),
            "checkout": self.checkout.to_dict(),
            "hidden": self.hidden,
            "isDefault": self.is_default,
        }


@dataclass_validate
@dataclass
class Option:
    label: str
    value: Value
    is_default: bool

    @classmethod
    def from_dict(cls, data: dict) -> "Option":
        return cls(
            label=data["label"],
            value=Value.from_dict(data["value"]),
            is_default=data["isDefault"],
        )

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "value": self.value.to_dict(),
            "isDefault": self.is_default,
        }


@dataclass_validate
@dataclass
class Portion:
    id: str
    title: str
    options: list[Option]
    description: str
    required: bool
    single_choice: bool
    sort_order: int

    @classmethod
    def from_dict(cls, data: dict) -> "Portion":
        return cls(
            id=data["id"],
            title=data["title"],
            options=[Option.from_dict(option) for option in data["options"]],
            description=data["description"],
            required=data["required"],
            single_choice=data["singleChoice"],
            sort_order=data["sortOrder"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "options": [option.to_dict() for option in self.options],
            "description": self.description,
            "required": self.required,
            "singleChoice": self.single_choice,
            "sortOrder": self.sort_order,
        }


@dataclass_validate
@dataclass
class Keyword:
    type: str
    name: str
    id: str
    label: str
    value: str | bool | None
    is_flag: bool
    is_badge: bool
    is_add_on: bool
    tags: list[str]
    icon: str | None
    icon_url: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "Keyword":
        return cls(
            type=data["type"],
            name=data["name"],
            id=data["id"],
            label=data["label"],
            value=data["value"],
            is_flag=data["isFlag"],
            is_badge=data["isBadge"],
            is_add_on=data["isAddOn"],
            tags=list(data["tags"].keys()) if data["tags"] else [],
            icon=data["icon"] if "icon" in data else None,
            icon_url=data["iconUrl"] if "iconUrl" in data else None,
        )

    def to_dict(self) -> dict:
        d = {
            "type": self.type,
            "name": self.name,
            "id": self.id,
            "label": self.label,
            "value": self.value,
            "isFlag": self.is_flag,
            "isBadge": self.is_badge,
            "isAddOn": self.is_add_on,
            "tags": {tag: True for tag in self.tags} if self.tags else [],
        }
        if self.icon is not None:
            d["icon"] = self.icon
        if self.icon_url is not None:
            d["iconUrl"] = self.icon_url
        return d


@dataclass_validate
@dataclass
class OptionsChoice:
    id: int
    name: str
    description: str
    keywords: list[Keyword]
    options: list[ProductItem]

    @classmethod
    def from_dict(cls, data: dict) -> "OptionsChoice":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            keywords=[Keyword.from_dict(keyword) for keyword in data["keywords"]],
            options=[ProductItem.from_dict(option) for option in data["options"]],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "keywords": [keyword.to_dict() for keyword in self.keywords],
            "options": [option.to_dict() for option in self.options],
        }


@dataclass_validate
@dataclass
class TillRequestOption:
    label: str
    value: str
    parts: list[str]

    @classmethod
    def from_dict(cls, data: dict) -> "TillRequestOption":
        return cls(
            label=data["label"],
            value=data["value"],
            parts=data["parts"],
        )

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "value": self.value,
            "parts": self.parts,
        }


@dataclass_validate
@dataclass
class TillRequestFilter:
    portion: list[str]

    @classmethod
    def from_dict(cls, data: dict) -> "TillRequestFilter":
        return cls(
            portion=data["portion"],
        )

    def to_dict(self) -> dict:
        return {
            "portion": self.portion,
        }


@dataclass_validate
@dataclass
class TillRequest:
    id: int | str
    name: str
    question: str
    required: bool
    single_choice: bool
    options: list[TillRequestOption]
    products: list[int]
    filter: TillRequestFilter
    title: str
    description: str

    @classmethod
    def from_dict(cls, data: dict) -> "TillRequest":
        return cls(
            id=data["id"],
            name=data["name"],
            question=data["question"],
            required=data["required"],
            single_choice=data["singleChoice"],
            options=[TillRequestOption.from_dict(option) for option in data["options"]],
            products=data["products"],
            filter=TillRequestFilter.from_dict(data["filter"]),
            title=data["title"],
            description=data["description"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "question": self.question,
            "required": self.required,
            "singleChoice": self.single_choice,
            "options": [option.to_dict() for option in self.options],
            "products": self.products,
            "filter": self.filter.to_dict(),
            "title": self.title,
            "description": self.description,
        }


@dataclass_validate
@dataclass
class TagOption:
    label: str
    value: str

    @classmethod
    def from_dict(cls, data: dict) -> "TagOption":
        return cls(
            label=data["label"],
            value=data["value"],
        )

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "value": self.value,
        }


@dataclass_validate
@dataclass
class Tag:
    id: str
    title: str
    options: list[TagOption]
    description: str
    required: bool
    single_choice: bool
    sort_order: int

    @classmethod
    def from_dict(cls, data: dict) -> "Tag":
        return cls(
            id=data["id"],
            title=data["title"],
            options=[TagOption.from_dict(option) for option in data["options"]],
            description=data["description"],
            required=data["required"],
            single_choice=data["singleChoice"],
            sort_order=data["sortOrder"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "options": [option.to_dict() for option in self.options],
            "description": self.description,
            "required": self.required,
            "singleChoice": self.single_choice,
            "sortOrder": self.sort_order,
        }


@dataclass_validate
@dataclass
class AddOn:
    id: int
    name: str
    hidden: bool
    sort_order: int
    item_groups: list[ItemGroup]
    sub_categories: None

    @classmethod
    def from_dict(cls, data: dict) -> "AddOn":
        return cls(
            id=data["id"],
            name=data["name"],
            hidden=data["hidden"],
            sort_order=data["sortOrder"],
            item_groups=[
                ItemGroup.from_dict(item_group) for item_group in data["itemGroups"]
            ],
            sub_categories=data["subCategories"] or None,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "hidden": self.hidden,
            "sortOrder": self.sort_order,
            "itemGroups": [item_group.to_dict() for item_group in self.item_groups],
            "subCategories": self.sub_categories or [],
        }


@dataclass_validate
@dataclass
class Linked:
    menu_id: int
    category_id: int
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> "Linked":
        return cls(
            menu_id=data["menuId"],
            category_id=data["categoryId"],
            name=data["name"],
        )

    def to_dict(self) -> dict:
        return {
            "menuId": self.menu_id,
            "categoryId": self.category_id,
            "name": self.name,
        }


@dataclass_validate
@dataclass
class Options:
    portion: Portion
    choices: list[OptionsChoice]
    swap: None
    till_requests: list[TillRequest]
    tags: list[Tag]
    add_ons: list[AddOn]
    linked: list[Linked]

    @classmethod
    def from_dict(cls, data: dict) -> "Options":
        return cls(
            portion=Portion.from_dict(data["portion"]),
            choices=[OptionsChoice.from_dict(choice) for choice in data["choices"]],
            swap=data["swap"],
            till_requests=[TillRequest.from_dict(tr) for tr in data["tillRequests"]],
            tags=[Tag.from_dict(tag) for tag in data["tags"]],
            add_ons=[AddOn.from_dict(add_on) for add_on in data["addOns"]],
            linked=[Linked.from_dict(link) for link in data["linked"]],
        )

    def to_dict(self) -> dict:
        return {
            "portion": self.portion.to_dict(),
            "choices": [choice.to_dict() for choice in self.choices],
            "swap": self.swap,
            "tillRequests": [tr.to_dict() for tr in self.till_requests],
            "tags": [tag.to_dict() for tag in self.tags],
            "addOns": [add_on.to_dict() for add_on in self.add_ons],
            "linked": [link.to_dict() for link in self.linked],
        }


@dataclass_validate
@dataclass
class ProductItem(Item):
    id: int
    name: str
    description: str
    checkout: Checkout
    calories: int | None
    is_out_of_stock: bool
    keywords: list[Keyword]
    course_id: int
    display_record_id: int
    alerts: None
    age_restriction: int
    related: list[int]
    options: Options
    sort_order: int
    show_price: bool
    sales_area_id: None

    @property
    def abv(self) -> float:
        abv_match = re.search(r"\d+\.?\d*(?=% abv)", self.description.lower())
        return float(abv_match.group(0)) if abv_match else 0.0
    
    @classmethod
    def from_dict(cls, data: dict) -> "ProductItem":
        return cls(
            **Item._base_kwargs(data),
            id=data["id"],
            name=data["name"],
            description=data["description"],
            checkout=Checkout.from_dict(data["checkout"]),
            calories=data["calories"],
            is_out_of_stock=data["isOutOfStock"],
            keywords=[Keyword.from_dict(keyword) for keyword in data["keywords"]],
            course_id=data["courseId"],
            display_record_id=data["displayRecordId"],
            alerts=data["alerts"],
            age_restriction=data["ageRestriction"],
            related=data["related"],
            options=Options.from_dict(data["options"]),
            sort_order=data["sortOrder"],
            show_price=data["showPrice"],
            sales_area_id=data["salesAreaId"] or None,
        )

    def to_dict(self) -> dict:
        item_dict = super().to_dict()
        return {
            **item_dict,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "checkout": self.checkout.to_dict(),
            "calories": self.calories,
            "isOutOfStock": self.is_out_of_stock,
            "keywords": [keyword.to_dict() for keyword in self.keywords],
            "courseId": self.course_id,
            "displayRecordId": self.display_record_id,
            "alerts": self.alerts,
            "ageRestriction": self.age_restriction,
            "related": self.related,
            "options": self.options.to_dict(),
            "sortOrder": self.sort_order,
            "showPrice": self.show_price,
            "salesAreaId": self.sales_area_id or [],
        }


@dataclass_validate
@dataclass
class TextItem(Item):
    text: str

    @classmethod
    def from_dict(cls, data: dict) -> "TextItem":
        return cls(
            **Item._base_kwargs(data),
            text=data["text"],
        )

    def to_dict(self) -> dict:
        item_dict = super().to_dict()
        return {
            **item_dict,
            "text": self.text,
        }


@dataclass_validate
@dataclass
class DividerItem(Item):
    @classmethod
    def from_dict(cls, data: dict) -> "DividerItem":
        return cls(**Item._base_kwargs(data))

    def to_dict(self) -> dict:
        item_dict = super().to_dict()
        return {
            **item_dict,
        }


@dataclass_validate
@dataclass
class AleType:
    key: str
    label: str
    hex_color: str

    @classmethod
    def from_dict(cls, data: dict) -> "AleType":
        return cls(
            key=data["key"],
            label=data["label"],
            hex_color=data["hexColor"],
        )

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "label": self.label,
            "hexColor": self.hex_color,
        }


@dataclass_validate
@dataclass
class Allergens:
    cereals_containing_gluten: list[str]

    @classmethod
    def from_dict(cls, data: dict) -> "Allergens":
        return cls(
            cereals_containing_gluten=(
                data["cerealsContainingGluten"].split(", ")
                if data["cerealsContainingGluten"] != "none"
                else []
            ),
        )

    def to_dict(self) -> dict:
        return {
            "cerealsContainingGluten": (
                ", ".join(self.cereals_containing_gluten)
                if self.cereals_containing_gluten
                else "none"
            ),
        }


@dataclass_validate
@dataclass
class AleItem(Item):
    id: int
    brewery: str
    name: str
    full_name: str
    type: AleType | None
    price_band: str
    abv: float
    units: float
    checkout: Checkout
    description: str
    coming_soon: bool
    sales_areas: None
    allergens: Allergens

    @classmethod
    def from_dict(cls, data: dict) -> "AleItem":
        return cls(
            **Item._base_kwargs(data),
            id=data["id"],
            brewery=data["brewery"],
            name=data["name"],
            full_name=data["fullName"],
            type=AleType.from_dict(data["type"]) if data["type"] is not None else None,
            price_band=data["priceBand"],
            abv=float(data["abv"]),
            units=float(data["units"]),
            checkout=Checkout.from_dict(data["checkout"]),
            description=data["description"],
            coming_soon=data["comingSoon"],
            sales_areas=data["salesAreas"] or None,
            allergens=Allergens.from_dict(data["allergens"]),
        )

    def to_dict(self) -> dict:
        item_dict = super().to_dict()
        return {
            **item_dict,
            "id": self.id,
            "brewery": self.brewery,
            "name": self.name,
            "fullName": self.full_name,
            "type": self.type.to_dict() if self.type is not None else None,
            "priceBand": self.price_band,
            "abv": self.abv,
            "units": self.units,
            "checkout": self.checkout.to_dict(),
            "description": self.description,
            "comingSoon": self.coming_soon,
            "salesAreas": self.sales_areas or [],
            "allergens": self.allergens.to_dict(),
        }


@dataclass_validate
@dataclass
class ItemGroup:
    name: str | None
    description: None
    items: list[Item]
    sort_order: int

    @classmethod
    def from_dict(cls, data: dict) -> "ItemGroup":
        return cls(
            name=data["name"],
            description=data["description"],
            items=[
                {
                    "product": ProductItem,
                    "text": TextItem,
                    "divider": DividerItem,
                    "ale": AleItem,
                }[item["itemType"]].from_dict(item)
                for item in data["items"]
            ],
            sort_order=data["sortOrder"],
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "items": [item.to_dict() for item in self.items],
            "sortOrder": self.sort_order,
        }


@dataclass_validate
@dataclass
class SubCategories:
    wo_white: str
    wo_red: str
    wo_rose: str
    wo_sparkling: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "SubCategories":
        return cls(
            wo_white=data["WO::white"],
            wo_red=data["WO::red"],
            wo_rose=data["WO::rose"],
            wo_sparkling=data["WO::spark"] if "WO::spark" in data else None,
        )

    def to_dict(self) -> dict:
        d = {
            "WO::white": self.wo_white,
            "WO::red": self.wo_red,
            "WO::rose": self.wo_rose,
        }
        if self.wo_sparkling is not None:
            d["WO::spark"] = self.wo_sparkling
        return d


@dataclass_validate
@dataclass
class Category:
    id: int
    name: str
    hidden: bool
    sort_order: int
    item_groups: list[ItemGroup]
    sub_categories: SubCategories | None

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        return cls(
            id=data["id"],
            name=data["name"],
            hidden=data["hidden"],
            sort_order=data["sortOrder"],
            item_groups=[ItemGroup.from_dict(ig) for ig in data["itemGroups"]],
            sub_categories=(
                SubCategories.from_dict(data["subCategories"])
                if data["subCategories"] != []
                else None
            ),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "hidden": self.hidden,
            "sortOrder": self.sort_order,
            "itemGroups": [ig.to_dict() for ig in self.item_groups],
            "subCategories": (
                self.sub_categories.to_dict() if self.sub_categories is not None else []
            ),
        }


@dataclass_validate
@dataclass
class Menu(MenuSummary):
    description: str | None
    image: str
    created: str
    updated: str
    categories: list[Category]
    version_id: int
    sort_order: int
    is_specials: bool

    @classmethod
    def from_dict(cls, data: dict) -> "Menu":
        return cls(
            **MenuSummary._base_kwargs(data),
            description=data["description"],
            image=data["image"],
            created=data["created"],
            updated=data["updated"],
            categories=[Category.from_dict(cat) for cat in data["categories"]],
            version_id=data["versionId"],
            sort_order=data["sortOrder"],
            is_specials=data["isSpecials"],
        )

    def to_dict(self) -> dict:
        menu_summary_dict = super().to_dict()
        return {
            **menu_summary_dict,
            "description": self.description,
            "image": self.image,
            "created": self.created,
            "updated": self.updated,
            "categories": [cat.to_dict() for cat in self.categories],
            "versionId": self.version_id,
            "sortOrder": self.sort_order,
            "isSpecials": self.is_specials,
        }

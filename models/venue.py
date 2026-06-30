import datetime

from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate


@dataclass_validate
@dataclass
class ClosureDates:
    closing_date: datetime.date | None
    closing_notes: str | None
    opening_date: datetime.date | None
    opening_notes: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "ClosureDates":
        return cls(
            closing_date=(
                datetime.date.fromisoformat(data["closingDate"])
                if data["closingDate"]
                else None
            ),
            closing_notes=data["closingNotes"],
            opening_date=(
                datetime.date.fromisoformat(data["openingDate"])
                if data["openingDate"]
                else None
            ),
            opening_notes=data["openingNotes"],
        )

    def to_dict(self) -> dict:
        return {
            "closingDate": self.closing_date.isoformat() if self.closing_date else None,
            "closingNotes": self.closing_notes,
            "openingDate": self.opening_date.isoformat() if self.opening_date else None,
            "openingNotes": self.opening_notes,
        }


@dataclass_validate
@dataclass
class Hotel:
    booking_url: str | None
    closure_dates: ClosureDates | None

    @classmethod
    def from_dict(cls, data: dict) -> "Hotel":
        return cls(
            booking_url=data["bookingUrl"],
            closure_dates=(
                ClosureDates.from_dict(data["closureDates"])
                if data["closureDates"]
                else None
            ),
        )

    def to_dict(self) -> dict:
        return {
            "bookingUrl": self.booking_url,
            "closureDates": (
                self.closure_dates.to_dict() if self.closure_dates else None
            ),
        }


@dataclass_validate
@dataclass
class SelectHandler:
    type: str

    @classmethod
    def from_dict(cls, data: dict) -> "SelectHandler":
        return cls(
            type=data["type"],
        )

    def to_dict(self) -> dict:
        return {
            "type": self.type,
        }


@dataclass_validate
@dataclass
class Country:
    name: str
    code: str

    @classmethod
    def from_dict(cls, data: dict) -> "Country":
        return cls(
            name=data["name"],
            code=data["code"],
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "code": self.code,
        }


@dataclass_validate
@dataclass
class Location:
    latitude: float
    longitude: float
    distance_tolerance: int

    @classmethod
    def from_dict(cls, data: dict) -> "Location":
        return cls(
            latitude=data["latitude"],
            longitude=data["longitude"],
            distance_tolerance=data["distanceTolerance"],
        )

    def to_dict(self) -> dict:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "distanceTolerance": self.distance_tolerance,
        }


@dataclass_validate
@dataclass
class Address:
    line1: str
    line2: str | None
    line3: str | None
    town: str
    county: str
    postcode: str
    country: Country
    location: Location

    @classmethod
    def from_dict(cls, data: dict) -> "Address":
        return cls(
            line1=data["line1"],
            line2=data["line2"],
            line3=data["line3"],
            town=data["town"],
            county=data["county"],
            postcode=data["postcode"],
            country=Country.from_dict(data["country"]),
            location=Location.from_dict(data["location"]),
        )

    def to_dict(self) -> dict:
        return {
            "line1": self.line1,
            "line2": self.line2,
            "line3": self.line3,
            "town": self.town,
            "county": self.county,
            "postcode": self.postcode,
            "country": self.country.to_dict(),
            "location": self.location.to_dict(),
        }


@dataclass_validate
@dataclass
class VenueSummary:
    franchise: str
    id: int
    venue_ref: int
    name: str
    status: str
    sub_type: str | None
    address: Address
    hotel: Hotel | None
    type: str
    is_closed: bool
    closure_dates: ClosureDates | None
    select_handler: SelectHandler

    @classmethod
    def _base_kwargs(cls, data: dict) -> dict:
        return dict(
            franchise=data["franchise"],
            id=data["id"],
            venue_ref=data["venueRef"],
            name=data["name"],
            status=data["status"],
            sub_type=data["subType"],
            address=Address.from_dict(data["address"]),
            hotel=Hotel.from_dict(data["hotel"]) if data["hotel"] else None,
            type=data["type"],
            is_closed=data["isClosed"],
            closure_dates=(
                ClosureDates.from_dict(data["closureDates"])
                if data["closureDates"]
                else None
            ),
            select_handler=SelectHandler.from_dict(data["selectHandler"]),
        )

    @classmethod
    def from_dict(cls, data: dict) -> "VenueSummary":
        return cls(**cls._base_kwargs(data))

    def to_dict(self) -> dict:
        return {
            "franchise": self.franchise,
            "id": self.id,
            "venueRef": self.venue_ref,
            "name": self.name,
            "status": self.status,
            "subType": self.sub_type,
            "address": self.address.to_dict(),
            "hotel": self.hotel.to_dict() if self.hotel else None,
            "type": self.type,
            "isClosed": self.is_closed,
            "closureDates": (
                self.closure_dates.to_dict() if self.closure_dates else None
            ),
            "selectHandler": self.select_handler.to_dict(),
        }


@dataclass_validate
@dataclass
class ContactDetails:
    email: str | None
    telephone: str | None
    website: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "ContactDetails":
        return cls(
            email=data.get("email") or None,
            telephone=data.get("telephone") or None,
            website=data.get("website") or None,
        )

    def to_dict(self) -> dict:
        return {
            "email": self.email or "",
            "telephone": self.telephone or "",
            "website": self.website or "",
        }


@dataclass_validate
@dataclass
class IncludeDrink:
    offset: float
    wine_offset: float

    @classmethod
    def from_dict(cls, data: dict) -> "IncludeDrink":
        return cls(
            offset=float(data["offset"]),
            wine_offset=float(data["wineOffset"]),
        )

    def to_dict(self) -> dict:
        return {
            "offset": self.offset,
            "wineOffset": self.wine_offset,
        }


@dataclass_validate
@dataclass
class Pricing:
    include_drink: IncludeDrink

    @classmethod
    def from_dict(cls, data: dict) -> "Pricing":
        return cls(
            include_drink=IncludeDrink.from_dict(data["includeDrink"]),
        )

    def to_dict(self) -> dict:
        return {
            "includeDrink": self.include_drink.to_dict(),
        }


@dataclass_validate
@dataclass
class Currency:
    code: str
    currency_code: str
    country_code: str
    symbol: str
    html_name: str
    html_number: str

    @classmethod
    def from_dict(cls, data: dict) -> "Currency":
        return cls(
            code=data["code"],
            currency_code=data["currencyCode"],
            country_code=data["countryCode"],
            symbol=data["symbol"],
            html_name=data["htmlName"],
            html_number=data["htmlNumber"],
        )

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "currencyCode": self.currency_code,
            "countryCode": self.country_code,
            "symbol": self.symbol,
            "htmlName": self.html_name,
            "htmlNumber": self.html_number,
        }


@dataclass_validate
@dataclass
class OpeningTime:
    open: str | None
    close: str | None
    label: str | None
    is_closed: bool

    @classmethod
    def from_dict(cls, data: dict) -> "OpeningTime":
        return cls(
            open=data["open"],
            close=data["close"],
            label=data["label"],
            is_closed=data["isClosed"],
        )

    def to_dict(self) -> dict:
        return {
            "open": self.open,
            "close": self.close,
            "label": self.label,
            "isClosed": self.is_closed,
        }


@dataclass_validate
@dataclass
class OpeningDays:
    monday: OpeningTime
    tuesday: OpeningTime
    wednesday: OpeningTime
    thursday: OpeningTime
    friday: OpeningTime
    saturday: OpeningTime
    sunday: OpeningTime

    @classmethod
    def from_dict(cls, data: dict) -> "OpeningDays":
        return cls(
            monday=OpeningTime.from_dict(data["mon"]),
            tuesday=OpeningTime.from_dict(data["tue"]),
            wednesday=OpeningTime.from_dict(data["wed"]),
            thursday=OpeningTime.from_dict(data["thu"]),
            friday=OpeningTime.from_dict(data["fri"]),
            saturday=OpeningTime.from_dict(data["sat"]),
            sunday=OpeningTime.from_dict(data["sun"]),
        )

    def to_dict(self) -> dict:
        return {
            "mon": self.monday.to_dict(),
            "tue": self.tuesday.to_dict(),
            "wed": self.wednesday.to_dict(),
            "thu": self.thursday.to_dict(),
            "fri": self.friday.to_dict(),
            "sat": self.saturday.to_dict(),
            "sun": self.sunday.to_dict(),
        }


@dataclass_validate
@dataclass
class OpeningTimes:
    days: OpeningDays
    dates: dict[str, OpeningTime] | None
    children: OpeningTime

    @classmethod
    def from_dict(cls, data: dict) -> "OpeningTimes":
        return cls(
            days=OpeningDays.from_dict(data["days"]),
            dates=(
                {k: OpeningTime.from_dict(v) for k, v in data["dates"].items()}
                if data["dates"]
                else None
            ),
            children=OpeningTime.from_dict(data["children"]),
        )

    def to_dict(self) -> dict:
        return {
            "days": self.days.to_dict(),
            "dates": (
                {k: v.to_dict() for k, v in self.dates.items()} if self.dates else []
            ),
            "children": self.children.to_dict(),
        }


@dataclass_validate
@dataclass
class PaymentMethod:
    label: str
    name: str
    enabled: bool

    @classmethod
    def from_dict(cls, data: dict) -> "PaymentMethod":
        return cls(
            label=data["label"],
            name=data["name"],
            enabled=data["enabled"],
        )

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "name": self.name,
            "enabled": self.enabled,
        }


@dataclass_validate
@dataclass
class PaymentMethods:
    card: PaymentMethod
    apple_pay: PaymentMethod
    google_pay: PaymentMethod
    paypal: PaymentMethod
    payit: PaymentMethod

    @classmethod
    def from_dict(cls, data: dict) -> "PaymentMethods":
        return cls(
            card=PaymentMethod.from_dict(data["card"]),
            apple_pay=PaymentMethod.from_dict(data["applePay"]),
            google_pay=PaymentMethod.from_dict(data["googlePay"]),
            paypal=PaymentMethod.from_dict(data["paypal"]),
            payit=PaymentMethod.from_dict(data["payit"]),
        )

    def to_dict(self) -> dict:
        return {
            "card": self.card.to_dict(),
            "applePay": self.apple_pay.to_dict(),
            "googlePay": self.google_pay.to_dict(),
            "paypal": self.paypal.to_dict(),
            "payit": self.payit.to_dict(),
        }


@dataclass_validate
@dataclass
class ApplePayConfig:
    merchant_id: str

    @classmethod
    def from_dict(cls, data: dict) -> "ApplePayConfig":
        return cls(
            merchant_id=data["merchantId"],
        )

    def to_dict(self) -> dict:
        return {
            "merchantId": self.merchant_id,
        }


@dataclass_validate
@dataclass
class GooglePayConfig:
    merchant_id: str
    gateway: str
    gateway_merchant_id: str

    @classmethod
    def from_dict(cls, data: dict) -> "GooglePayConfig":
        return cls(
            merchant_id=data["merchantId"],
            gateway=data["gateway"],
            gateway_merchant_id=data["gatewayMerchantId"],
        )

    def to_dict(self) -> dict:
        return {
            "merchantId": self.merchant_id,
            "gateway": self.gateway,
            "gatewayMerchantId": self.gateway_merchant_id,
        }


@dataclass_validate
@dataclass
class PaymentConfig:
    methods: PaymentMethods
    apple_pay: ApplePayConfig
    google_pay: GooglePayConfig

    @classmethod
    def from_dict(cls, data: dict) -> "PaymentConfig":
        return cls(
            methods=PaymentMethods.from_dict(data["methods"]),
            apple_pay=ApplePayConfig.from_dict(data["applePay"]),
            google_pay=GooglePayConfig.from_dict(data["googlePay"]),
        )

    def to_dict(self) -> dict:
        return {
            "methods": self.methods.to_dict(),
            "applePay": self.apple_pay.to_dict(),
            "googlePay": self.google_pay.to_dict(),
        }


@dataclass_validate
@dataclass
class MenuURL:
    dairy_free: str | None
    gluten_free: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "MenuURL":
        return cls(
            dairy_free=data.get("dairyFree"),
            gluten_free=data.get("glutenFree"),
        )

    def to_dict(self) -> dict:
        return {
            "dairyFree": self.dairy_free,
            "glutenFree": self.gluten_free,
        }


@dataclass_validate
@dataclass
class SalesArea:
    id: int
    name: str
    friendly: str | None
    description: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "SalesArea":
        return cls(
            id=data["id"],
            name=data["name"],
            friendly=data.get("friendly"),
            description=data.get("description"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "friendly": self.friendly,
            "description": self.description,
        }


@dataclass_validate
@dataclass
class Venue(VenueSummary):
    thumbnail: str
    display_images: list[str]
    allergens_url: str
    can_place_order: bool
    coming_soon: bool
    contact_details: ContactDetails
    pricing: Pricing
    currency: Currency
    facilities: list
    opening_times: OpeningTimes
    payment_config: PaymentConfig
    menu_url: MenuURL
    sales_areas: list[SalesArea]
    ordering_enabled: bool

    @classmethod
    def from_dict(cls, data: dict) -> "Venue":
        return cls(
            **VenueSummary._base_kwargs(data),
            thumbnail=data["thumbnail"],
            display_images=data["displayImages"],
            allergens_url=data["allergensUrl"],
            can_place_order=data["canPlaceOrder"],
            coming_soon=data["comingSoon"],
            contact_details=ContactDetails.from_dict(data["contactDetails"]),
            pricing=Pricing.from_dict(data["pricing"]),
            currency=Currency.from_dict(data["currency"]),
            facilities=data["facilities"],
            opening_times=OpeningTimes.from_dict(data["openingTimes"]),
            payment_config=PaymentConfig.from_dict(data["paymentConfig"]),
            menu_url=MenuURL.from_dict(data["menuUrl"]),
            sales_areas=[SalesArea.from_dict(sa) for sa in data["salesAreas"]],
            ordering_enabled=data["orderingEnabled"],
        )

    def to_dict(self) -> dict:
        venue_summary_dict = super().to_dict()
        return {
            **venue_summary_dict,
            "thumbnail": self.thumbnail,
            "displayImages": self.display_images,
            "allergensUrl": self.allergens_url,
            "canPlaceOrder": self.can_place_order,
            "comingSoon": self.coming_soon,
            "contactDetails": self.contact_details.to_dict(),
            "pricing": self.pricing.to_dict(),
            "currency": self.currency.to_dict(),
            "facilities": self.facilities,
            "openingTimes": self.opening_times.to_dict(),
            "paymentConfig": self.payment_config.to_dict(),
            "menuUrl": self.menu_url.to_dict(),
            "salesAreas": [sa.to_dict() for sa in self.sales_areas],
            "orderingEnabled": self.ordering_enabled,
        }

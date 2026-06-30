import datetime
import json
import uuid

from peewee import (
    CharField,
    DateTimeField,
    ForeignKeyField,
    Model,
    SqliteDatabase,
    TextField,
    UUIDField,
)

db = SqliteDatabase("spoons_api.db")


class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        database = db


class JSONField(TextField):
    def db_value(self, value: dict | None) -> str | None:
        if value is None:
            return None
        return json.dumps(value, separators=(",", ":"))

    def python_value(self, value: str | None) -> dict | None:
        if value is None:
            return None
        return json.loads(value)


class CacheObject(BaseModel):
    slug = CharField(unique=True)


class Response(BaseModel):
    cache_object = ForeignKeyField(CacheObject, backref="responses")
    response_data = JSONField()
    timestamp = DateTimeField(
        default=datetime.datetime.now,
        index=True,
    )


def _initialise_db():
    db.connect(reuse_if_open=True)
    db.create_tables([CacheObject, Response], safe=True)


def get_cached_response(
    slug: str,
    max_age: datetime.timedelta | None = None,
) -> dict | None:
    """
    Retrieve the latest cached response for a slug.

    If max_age is None (default), always returns the latest response.
    Otherwise, only returns it if it is newer than max_age.
    """
    _initialise_db()

    response = (
        Response.select()
        .join(CacheObject)
        .where(CacheObject.slug == slug)
        .order_by(Response.timestamp.desc())
        .first()
    )

    if response is None:
        return None

    if max_age is not None:
        age = datetime.datetime.now() - response.timestamp
        if age > max_age:
            return None

    return response.response_data


def cache_response(slug: str, response_data: dict) -> None:
    """Cache a response for the given slug."""
    _initialise_db()

    cache_object, _ = CacheObject.get_or_create(slug=slug)
    Response.create(cache_object=cache_object, response_data=response_data)

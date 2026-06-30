import datetime
import requests
import tomllib
import urllib.parse

from cache import get_cached_response, cache_response

from tenacity import retry, wait_exponential, retry_if_exception


def _is_retryable(exc: Exception) -> bool:
    return isinstance(exc, requests.HTTPError) and exc.response.status_code in {
        403,
        429,
    }


with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
    API_VERSION = data["project"]["version"]


API_ENDPOINT = "https://ca.jdw-apps.net/api/v0.1/"
API_HEADERS = {
    "Authorization": "Bearer 1|SFS9MMnn5deflq0BMcUTSijwSMBB4mc7NSG2rOhqb2765466",
    "User-Agent": f"Wetherspoons API Client/{API_VERSION}",
}


@retry(
    retry=retry_if_exception(_is_retryable),
    wait=wait_exponential(multiplier=1, min=5, max=50),
)
def request(
    slug: str, use_cache=True, max_age: datetime.timedelta | None = None
) -> dict:
    slug = slug.lstrip("/")
    if use_cache:
        cached_response = get_cached_response(slug, max_age=max_age)
        if cached_response is not None:
            return cached_response
    request_url = urllib.parse.urljoin(API_ENDPOINT, slug)
    response = requests.get(request_url, headers=API_HEADERS)
    response.raise_for_status()
    json_data = response.json()
    cache_response(slug, json_data)
    return json_data

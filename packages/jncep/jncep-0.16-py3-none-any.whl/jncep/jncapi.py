import json
import re
from urllib.parse import urlparse

from addict import Dict as Addict
import requests
import requests_toolbelt.utils.dump

IMG_URL_BASE = "https://d2dq7ifhe7bu0f.cloudfront.net"
JNC_URL_BASE = "https://j-novel.club"
API_JNC_URL_BASE = "https://api.j-novel.club"

COMMON_API_HEADERS = {"accept": "application/json", "content-type": "application/json"}


def login(email, password):
    url = f"{API_JNC_URL_BASE}/api/users/login?include=user"
    headers = COMMON_API_HEADERS
    payload = {"email": email, "password": password}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    r.raise_for_status()

    access_token_cookie = r.cookies["access_token"]
    access_token = access_token_cookie[4 : access_token_cookie.index(".")]

    return access_token


def logout(token):
    url = f"{API_JNC_URL_BASE}/api/users/logout"
    headers = {"authorization": token, **COMMON_API_HEADERS}
    r = requests.post(url, headers=headers)
    r.raise_for_status()


def fetch_metadata(token, slug):
    headers = {"authorization": token, **COMMON_API_HEADERS}

    where, req_type = slug
    if req_type == "PART":
        res_type = "parts"
        include = [{"serie": ["volumes", "parts"]}, "volume"]
    elif req_type == "VOLUME":
        res_type = "volumes"
        include = [{"serie": ["volumes", "parts"]}, "parts"]
    else:
        res_type = "series"
        include = ["volumes", "parts"]

    url = f"{API_JNC_URL_BASE}/api/{res_type}/findOne"

    qfilter = {
        "where": {"titleslug": where},
        "include": include,
    }
    payload = {"filter": json.dumps(qfilter)}

    r = requests.get(url, headers=headers, params=payload)
    r.raise_for_status()

    return Addict(r.json())


def fetch_content(token, part_id):
    url = f"{API_JNC_URL_BASE}/api/parts/{part_id}/partData"
    headers = {"authorization": token, **COMMON_API_HEADERS}
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    return r.json()["dataHTML"]


def fetch_image_from_cdn(url):
    r = requests.get(url)
    r.raise_for_status()
    # should be JPEG
    return r.content


def slug_from_url(url):
    pu = urlparse(url)

    if pu.scheme == "":
        raise ValueError(f"Not a URL: {url}")
    # path is: /c/<slug>/...  or /v/<slug>/... or /s/<slug>/...
    # for c_hapter, v_olume, s_erie
    m = re.match(r"^/(v|c|s)/(.+?)(?:(?=/)|$)", pu.path)
    if not m:
        raise ValueError(f"Invalid path for URL: {url}")

    return m.group(2), _to_const(m.group(1))


def url_from_slug(series_slug):
    return f"{JNC_URL_BASE}/s/{series_slug}"


def _to_const(req_type):
    if req_type == "c":
        return "PART"
    elif req_type == "v":
        return "VOLUME"
    else:
        return "NOVEL"


def _dump(response):
    data = requests_toolbelt.utils.dump.dump_response(response)
    print(data.decode("utf-8"))

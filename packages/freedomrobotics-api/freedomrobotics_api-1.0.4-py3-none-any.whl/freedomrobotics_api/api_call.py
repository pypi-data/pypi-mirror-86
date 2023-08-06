import json
import os

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=10, read=10, connect=10, backoff_factor=0.3, status_forcelist=(500, 502, 504))
adapter = HTTPAdapter(max_retries=retry, pool_connections=1000, pool_maxsize=1000)
session.mount('http://', adapter)
session.mount('https://', adapter)


URL = "https://api.freedomrobotics.ai"
TOKEN = None
SECRET = None


def api_auth(token, secret, url=None):
    global TOKEN, SECRET, URL
    TOKEN = token
    SECRET = secret
    if url is not None:
        URL = url


def api_call(method, path, data=None, params=None, no_auth=False, raw=False):
    if no_auth:
        auth_headers = {}
    else:
        auth_headers = {
            "mc_token": TOKEN,
            "mc_secret": SECRET
        }

    url = URL.strip("/") + "/" + path.strip("/")
    if method == "GET":
        r = session.get(
            url,
            headers=auth_headers,
            params=params
        )
    elif method == "POST":
        r = session.post(
            url,
            headers=auth_headers,
            json=data
        )
    elif method == "PUT":
        r = session.put(
            url,
            headers=auth_headers,
            json=data
        )

    r.raise_for_status()

    try:
        if raw:
            return r.text
        else:
            return r.json()
    except ValueError:
        raise Exception("Error parsing API response to JSON: [%d] %s" % (r.status_code, r.text))

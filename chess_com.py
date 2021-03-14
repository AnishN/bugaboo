import json
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

session = requests.Session()
retries = Retry(
    total=10,
    read=10,
    connect=10,
    redirect=10,
    status=10,
    backoff_factor=2.0,
    status_forcelist=[104, 429, 500, 502, 503, 504],
)
session.mount('https://', HTTPAdapter(max_retries=retries))

def fetch_game(game):
    base_url = "https://chess.com/callback/live/game/{0}"
    url = base_url.format(game)
    resp = session.get(url, verify=True)
    if resp.status_code != 200:
        raise ValueError("Could not get game (Status Code Error: {0})".format(resp.status_code))
    return resp.json()
import os
import json
from urllib.parse import urlunsplit, quote
from requests_oauthlib import requests


class Mastodon:
    def __init__(self, access_token, host_domain):
        self.host_domain = host_domain
        self.session = requests.Session()
        self.session.headers.update({"Authorization": "Bearer "+access_token})

    def _build_url(self, path):
        return urlunsplit(["https", self.host_domain, path, "", ""])

    def _request(self, method, url, data=None, params=None):
        kwargs = {
            "data": data or {},
            "params": params or {}
        }
        resp = self.session.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp

    def toot(self, text, reply_target_id, reply_user):
        url = self._build_url("/api/v1/statuses")
        if not reply_target_id == None:
            data = {
                "status": text+" #獅子の黄金",
                "in_reply_to_id": reply_target_id
            }
        else:
            data = {
                "status": reply_user+"\n"+text+" #獅子の黄金"
            }
        return self._request("post", url, data=data)

    def verify_credentials(self):
        url = self._build_url("/api/v1/accounts/verify_credentials")
        return self._request("get", url)


def get_keys_data(root_dir):
    file_path = root_dir+"/keys.json"
    with open(file_path, "r") as input:
        text = input.read()
    return json.loads(text)


def add_client_keys(root_dir, current_keys, host_domain, client_keys):
    file_path = root_dir+"/keys.json"
    current_keys[host_domain] = client_keys
    with open(file_path, "w") as output:
        output.write(json.dumps(current_keys))


def get_client_keys(root_dir, host_domain):
    keys = get_keys_data(root_dir)
    if not host_domain in keys:
        client_keys = register_app(host_domain, "獅子の黄金 アカウント確認",
                                   "https://app.odakyu.app/regulusaurum",
                                   "urn:ietf:wg:oauth:2.0:oob\nhttps://app.odakyu.app/regulusaurum/done",
                                   "read:accounts")
        add_client_keys(root_dir, keys, host_domain, client_keys)
        return client_keys
    else:
        return keys[host_domain]


def register_app(host_domain, client_name, website_url, redirect_uris, scopes):
    data = {
        "client_name": client_name,
        "website": website_url,
        "redirect_uris": redirect_uris,
        "scopes": scopes
    }
    response = requests.post(
        "https://{host}/api/v1/apps".format(host=host_domain), data=data)
    response.raise_for_status()
    result = response.json()
    return [result["client_id"], result["client_secret"]]


def generate_oauth_url(host_domain, client_id, redirect_uri, scopes):
    return "https://"+host_domain+"/oauth/authorize?response_type=code&client_id="+client_id+"&redirect_uri="+quote(redirect_uri)+"&scope="+quote(scopes)

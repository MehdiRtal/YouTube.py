import requests
import time
import json
import os
import pathlib


_cache_dir = pathlib.Path(__file__).parent.resolve() / "__cache__"
_tokens_file = os.path.join(_cache_dir, "tokens.json")

_client_id = "861556708454-d6dlm3lh05idd8npek18k6be8ba3oc68.apps.googleusercontent.com"
_client_secret = "SboVhoG9s0rNafixCSGGKXAT"

_clients = {
    "WEB": {
        "context": {
            "client": {
                "clientName": "WEB",
                "clientVersion": "2.20230530.05.00"
            }
        },
        "User-Agent": "Mozilla/5.0",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },
    "WEB_EMBED": {
        "context": {
            "client": {
                "clientName": "WEB_EMBEDDED_PLAYER",
                "clientVersion": "2.20230530.05.00",
                "clientScreen": "EMBED"
            }
        },
        "User-Agent": "Mozilla/5.0",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },
    "WEB_MUSIC": {
        "context": {
            "client": {
                "clientName": "WEB_REMIX",
                "clientVersion": "2.20230530.05.00",
            }
        },
        "header": {
            "User-Agent": "Mozilla/5.0"
        },
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },
    "WEB_CREATOR": {
        "context": {
            "client": {
                "clientName": "WEB_CREATOR",
                "clientVersion": "2.20230530.05.00",
            }
        },
        "User-Agent": "Mozilla/5.0",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },

    "ANDROID": {
        "context": {
            "client": {
                "clientName": "ANDROID",
                "clientVersion": "18.21.34",
                "androidSdkVersion": 33
            }
        },
        "User-Agent": "com.google.android.youtube/",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },
    "ANDROID_EMBED": {
        "context": {
            "client": {
                "clientName": "ANDROID_EMBEDDED_PLAYER",
                "clientVersion": "18.21.34",
                "clientScreen": "EMBED",
                "androidSdkVersion": 33,
            }
        },
        "User-Agent": "com.google.android.youtube/",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },
    "ANDROID_MUSIC": {
        "context": {
            "client": {
                "clientName": "ANDROID_MUSIC",
                "clientVersion": "6.03.51",
                "androidSdkVersion": 33
            }
        },
        "User-Agent": "com.google.android.apps.youtube.music/",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },
    "ANDROID_CREATOR": {
        "context": {
            "client": {
                "clientName": "ANDROID_CREATOR",
                "clientVersion": "23.20.100",
                "androidSdkVersion": 33,
            }
        },
        "User-Agent": "com.google.android.apps.youtube.creator/",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },

    "IOS": {
        "context": {
            "client": {
                "clientName": "IOS",
                "clientVersion": "18.21.34",
                "deviceModel": "iPhone14,3"
            }
        },
        "User-Agent": "com.google.ios.youtube/",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },
    "IOS_EMBED": {
        "context": {
            "client": {
                "clientName": "IOS_MESSAGES_EXTENSION",
                "clientVersion": "18.21.34",
                "deviceModel": "iPhone14,3"
            }
        },
        "User-Agent": "com.google.ios.youtube/",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },
    "IOS_MUSIC": {
        "context": {
            "client": {
                "clientName": "IOS_MUSIC",
                "clientVersion": "6.03.51",
                "deviceModel": "iPhone14,3"
            }
        },
        "User-Agent": "com.google.ios.youtubemusic/",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },
    "IOS_CREATOR": {
        "context": {
            "client": {
                "clientName": "IOS_CREATOR",
                "clientVersion": "23.20.100",
                "deviceModel": "iPhone14,3",
            }
        },
        "User-Agent": "com.google.ios.ytcreator/",
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
    },
}

class InnerTube:
    def __init__(self, client: str, proxy: str = None, use_oauth: bool = False, allow_cache: bool = True):
        self.base_url = "https://www.youtube.com/youtubei/v1"
        self.base_data = {
            "context": _clients[client]["context"]
        }
        self.base_headers = {
            "User-Agent": _clients[client]["User-Agent"]
        }
        self.base_params = {
            "key": _clients[client]["key"]
        }
        self.proxy = proxy
        self.access_token = None
        self.refresh_token = None
        self.expires = None
        self.use_oauth = use_oauth
        self.allow_cache = allow_cache
        if self.use_oauth and self.allow_cache:
            if os.path.exists(_tokens_file):
                with open(_tokens_file) as f:
                    data = json.load(f)
                    self.access_token = data["access_token"]
                    self.refresh_token = data["refresh_token"]
                    self.expires = data["expires"]
                    self.refresh_bearer_token()

    def cache_tokens(self):
        if not self.allow_cache:
            return
        data = {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires": self.expires
        }
        if not os.path.exists(_cache_dir):
            os.mkdir(_cache_dir)
        with open(_tokens_file, "w") as f:
            json.dump(data, f)

    def refresh_bearer_token(self, force=False):
        if self.expires > time.time() and not force:
            return
        start_time = int(time.time() - 30)
        data = {
            "client_id": _client_id,
            "client_secret": _client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        response = requests.post("https://oauth2.googleapis.com/token", json=data)
        response_data = response.json()
        self.access_token = response_data["access_token"]
        self.expires = start_time + response_data["expires_in"]
        self.cache_tokens()

    def fetch_bearer_token(self):
        start_time = int(time.time() - 30)
        data = {
            "client_id": _client_id,
            "scope": "https://www.googleapis.com/auth/youtube"
        }
        response = requests.post("https://oauth2.googleapis.com/device/code", json=data)
        response_data = response.json()
        verification_url = response_data["verification_url"]
        user_code = response_data["user_code"]
        print(f"Please open {verification_url} and input code {user_code}")
        input("Press enter when you have completed this step.")
        data = {
            "client_id": _client_id,
            "client_secret": _client_secret,
            "device_code": response_data["device_code"],
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        }
        response = requests.post("https://oauth2.googleapis.com/token", json=data)
        response_data = response.json()
        self.access_token = response_data["access_token"]
        self.refresh_token = response_data["refresh_token"]
        self.expires = start_time + response_data["expires_in"]
        self.cache_tokens()

    def __api(self, endpoint: str, params: dict = {}, data: dict = {}):
        params.update(self.base_params)
        data.update(self.base_data)
        headers = self.base_headers.copy()
        if self.use_oauth:
            if self.access_token:
                self.refresh_bearer_token()
                headers.update({"Authorization": f"Bearer {self.access_token}"})
            else:
                self.fetch_bearer_token()
                headers.update({"Authorization": f"Bearer {self.access_token}"})
        response = requests.post(
            f"{self.base_url}{endpoint}",
            params=params,
            headers=headers,
            json=data,
            proxies={"https": f"http://{self.proxy}"} if self.proxy else None
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()

    def player(self, video_id: str):
        params = {
            "videoId": video_id
        }
        return self.__api("/player", params=params)

    def search(self, query: str):
        params = {
            "query": query
        }
        return self.__api("/search", params=params)

    def verify_age(self, video_id: str):
        data = {
            "nextEndpoint": {
                "urlEndpoint": {
                    "url": f"/watch?v={video_id}"
                }
            },
            "setControvercy": True
        }
        result = self.__api("/verify_age", data=data)
        return result

    def get_transcript(self, video_id: str):
        params = {
            "videoId": video_id,
        }
        result = self.__api("/get_transcript", params=params)
        return result
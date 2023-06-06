import requests


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
    def __init__(self, client: str, proxy: str = None):
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
    
    def _api(self, endpoint: str, params: dict = {}, data: dict = {}):
        params.update(self.base_params)
        data.update(self.base_data)
        response = requests.post(
            f"{self.base_url}{endpoint}",
            params=params,
            headers=self.base_headers,
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
        return self._api("/player", params=params)

    def search(self, query: str):
        params = {
            "query": query
        }
        return self._api("/search", params=params)

    def verify_age(self, video_id: str):
        data = {
            "nextEndpoint": {
                "urlEndpoint": {
                    "url": f"/watch?v={video_id}"
                }
            },
            "setControvercy": True
        }
        result = self._api("/verify_age", data=data)
        return result

    def get_transcript(self, video_id: str):
        params = {
            "videoId": video_id,
        }
        result = self._api("/get_transcript", params=params)
        return result
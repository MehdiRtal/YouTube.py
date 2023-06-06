import re

from innertube import InnerTube
from models import Video


class Youtube:
    def __init__(self, client: str = "ANDROID_CREATOR", proxy: str = None, use_oauth: bool = False, allow_cache: bool = True):
        self.it = InnerTube(client=client, proxy=proxy, use_oauth=use_oauth, allow_cache=allow_cache)

    def _get_video_id(self, url: str):
        return re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url).group(1)

    def get_video(self, url: str):
        video = self.it.player(self._get_video_id(url))
        if video["playabilityStatus"]["status"] != "OK":
            raise Exception(video["playabilityStatus"]["reason"])
        return Video(**video)
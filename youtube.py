import re

from innertube import InnerTube
from exceptions import LoginRequired, VideoUnavailable, VideoAgeRestricted, VideoPrivate
from models import Video


class YouTube:
    def __init__(self, client: str = "ANDROID_CREATOR", proxy: str = None, use_oauth: bool = False, allow_cache: bool = True):
        self.it = InnerTube(client=client, proxy=proxy, use_oauth=use_oauth, allow_cache=allow_cache)

    def __get_video_id(self, url: str):
        return re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url).group(1)

    def get_video(self, url: str):
        video = self.it.player(self.__get_video_id(url))
        status = video["playabilityStatus"]["status"]
        if status == "OK":
            return Video(**video)
        else:
            reason = video["playabilityStatus"]["reason"]
            if status == "LOGIN_REQUIRED":
                if reason == "Sorry, this content is age-restricted" or reason == "This video may be inappropriate for some users." or reason == "Sign in to confirm your age":
                    raise VideoAgeRestricted(reason)
                elif reason == "This is a private video. Please sign in to verify that you may see it.":
                    raise VideoPrivate(reason)
                else:
                    raise LoginRequired(reason)
            elif status == "UNPLAYABLE":
                if reason == "Join this channel to get access to members-only content like this video, and other exclusive perks.":
                    raise VideoPrivate(reason)
                else:
                    raise VideoUnavailable(reason)
            elif status == "ERROR":
                raise VideoUnavailable(reason)
            elif status == "CONTENT_CHECK_REQUIRED":
                raise VideoAgeRestricted(reason)
            else:
                raise VideoUnavailable(reason)
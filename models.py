from pydantic import BaseModel, Field, AliasPath
from typing import List


class Thumbnail(BaseModel):
    url: str
    width: int
    height: int

class Stream(BaseModel):
    itag: int
    mime_type: str = Field(validation_alias="mimeType")
    audio_sample_rate: int = Field(None, validation_alias="audioSampleRate")
    quality: str = Field(None, validation_alias="qualityLabel")
    fps: int = Field(None)
    url: str

class StreamType(BaseModel):
    adaptive: List[Stream] = Field(validation_alias="adaptiveFormats",)
    legacy: List[Stream] = Field(None, validation_alias="formats")

class Video(BaseModel):
    title : str = Field(validation_alias=AliasPath("videoDetails", "title"))
    description: str = Field(validation_alias=AliasPath("videoDetails", "shortDescription"))
    author : str = Field(validation_alias=AliasPath("videoDetails", "author"))
    views : int = Field(validation_alias=AliasPath("videoDetails", "viewCount"))
    thumbnails: List[Thumbnail] = Field(validation_alias=AliasPath("videoDetails", "thumbnail", "thumbnails"))
    streams: StreamType = Field(validation_alias="streamingData")
    is_live: bool = Field(validation_alias=AliasPath("videoDetails", "isLive"))
from pydantic import BaseModel, Field
from typing import List


class VideoThumbnails(BaseModel):
    url: str
    width: int
    height: int

class VideoThumbnail(BaseModel):
    thumbnails: List[VideoThumbnails]

class VideoDetails(BaseModel):
    title: str
    description: str = Field(alias="shortDescription")
    author: str
    views: int = Field(alias="viewCount")
    thumbnail: VideoThumbnail
    
class VideoStream(BaseModel):
    itag: int
    mime_type: str = Field(alias="mimeType")
    audio_sample_rate: int = Field(None, alias="audioSampleRate")
    quality: str = Field(None, alias="qualityLabel")
    fps: int = None
    url: str

class VideoStreamDetails(BaseModel):
    adaptive_format: List[VideoStream] = Field(alias="adaptiveFormats")
    legacy_format: List[VideoStream] = Field(None, alias="formats")

class Video(BaseModel):  
    details: VideoDetails = Field(alias="videoDetails")
    streams: VideoStreamDetails = Field(alias="streamingData")
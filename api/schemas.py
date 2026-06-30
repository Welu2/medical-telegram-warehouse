from pydantic import BaseModel
from typing import List


class TopProduct(BaseModel):
    product: str
    mentions: int


class ChannelActivity(BaseModel):
    channel_name: str
    date: str
    posts: int


class MessageSearch(BaseModel):
    message_id: int
    channel_name: str
    message: str
    date: str


class VisualStats(BaseModel):
    channel_name: str
    total_images: int
    detections: int
from pydantic import BaseModel
from typing import Union


class SocketMessage(BaseModel):
    """
    SocketMessage represents the action and data that is passed in and passed out of a socket connection
    """
    action: str
    data: dict = {}


class ChannelSocketMessage(SocketMessage):
    """
    SocketMessage represents the action and data that is passed in and passed out of a socket connection
    """
    channel: str = None


class APIGatewayMessage:
    connection_id: str
    event: str
    message: Union[dict, str]

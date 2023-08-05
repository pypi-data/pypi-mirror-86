from pydantic import BaseModel


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
    channel: str

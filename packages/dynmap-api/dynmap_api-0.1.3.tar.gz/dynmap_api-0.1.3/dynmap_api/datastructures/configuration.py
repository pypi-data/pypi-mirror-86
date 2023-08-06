from pydantic import BaseModel
from typing import List, Optional

from .world import World


class ClientConfiguration(BaseModel):
    """Represents configuration data sent by dynmap backend on connection"""

    updaterate: int
    chatlengthlimit: int
    confighash: int
    defaultmap: str
    title: str
    defaultzoom: int
    allowwebchat: bool
    allowchat: bool
    webchat_interval: Optional[int]
    loggedin: bool
    coreversion: str
    webchat_requires_login: Optional[bool]
    login_enabled: Optional[bool]
    maxcount: int
    dynmapversion: str
    cyrillic: bool
    webprefix: str
    defaultworld: str

    worlds: List[World]
    components: List[dict]

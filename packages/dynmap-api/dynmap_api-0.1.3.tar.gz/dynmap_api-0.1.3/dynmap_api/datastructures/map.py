from pydantic import BaseModel
from typing import List, Optional

class Map(BaseModel):
    
    inclination: int
    nightandday: bool
    image_format: Optional[str]
    shader: str
    compassview: str
    prefix: str
    icon: Optional[str]
    scale: int
    azimuth: int
    type: str
    title: str
    lighting: str
    backgroundday: Optional[str]
    bigmap: bool
    maptoworld: List[int]
    worldtomap: List[int]
    protected: bool
    background: Optional[str]
    mapzoomout: int
    boostzoom: int
    name: str
    backgroundnight: Optional[str]
    perspective: str
    mapzoomin: int
    

from pydantic import BaseModel
from typing import Optional

class Data(BaseModel):
    username: str
    date: str
    time: str
    activity: Optional[int]
    acceleration_x : float
    acceleration_y : float
    acceleration_z : float
    gyro_x : float
    gyro_y : float
    gyro_z : float
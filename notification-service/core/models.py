from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field


class AlarmNotification(BaseModel):
    alarm: int
    ts: datetime = Field(default_factory=datetime.now)
    notification_type: Literal[
        "deactivated",
        "activated",
        "triggered"
    ]

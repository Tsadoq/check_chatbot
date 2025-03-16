import datetime
from typing import List

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Representation of search score.
    """
    status: str = Field(default='up', alias='status', examples=['up'])
    time: List[float] = Field(
        default=datetime.datetime.now(datetime.UTC).strftime(format='%Y-%m-%dT%H:%M:%S.%fZ'),
        alias='time',
        examples=['1996-01-08T08:01:30.123336Z'],
    )

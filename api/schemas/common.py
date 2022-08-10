from pydantic import BaseModel
from typing import Optional


class StatusResponse(BaseModel):
    success: bool
    message: Optional[str] = None
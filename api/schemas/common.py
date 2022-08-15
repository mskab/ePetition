from typing import Optional

from pydantic import BaseModel


class StatusResponse(BaseModel):
    success: bool
    message: Optional[str] = None

from sqlite3 import Date
from typing import List, Optional

from pydantic import BaseModel


class StatusResponse(BaseModel):
    success: bool
    message: Optional[str] = None


class PaginationRequest(BaseModel):
    offset: int = 0
    limit: int = 4


class FilteringDateRequest(BaseModel):
    start: Optional[Date]
    end: Optional[Date]


class FilteringRequest(BaseModel):
    creation_date: Optional[FilteringDateRequest]
    due_date: Optional[FilteringDateRequest]
    status: Optional[List[str]]


class OrderingRequest(BaseModel):
    order: Optional[str]
    by: Optional[str]


class ResponseModificators(BaseModel):
    pagination: PaginationRequest
    ordering: Optional[List[OrderingRequest]]
    filtering: Optional[FilteringRequest]

from pydantic import BaseModel
from typing import List, Optional

class NotionTableRow(BaseModel):
    id: str
    title: str
    properties: dict

class NotionResponse(BaseModel):
    results: List[NotionTableRow]
    next_cursor: Optional[str] = None
    has_more: bool = False

class NotionRequest(BaseModel):
    database_id: str
    filter: Optional[dict] = None
    sorts: Optional[List[dict]] = None
    start_cursor: Optional[str] = None
    page_size: Optional[int] = None
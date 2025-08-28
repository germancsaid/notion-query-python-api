from pydantic import BaseModel
from typing import List, Optional

class NotionTable(BaseModel):
    id: str
    title: str
    properties: dict

class NotionResponse(BaseModel):
    results: List[NotionTable]
    next_cursor: Optional[str] = None
    has_more: bool = False
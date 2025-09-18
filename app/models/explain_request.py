from pydantic import BaseModel
from typing import Optional

class ExplainRequest(BaseModel):
    url: str
    figure_id: Optional[str] = None
    section: Optional[str] = None

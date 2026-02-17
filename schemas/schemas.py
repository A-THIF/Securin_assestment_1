from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CVESchema(BaseModel):
    cve_id: str
    description: Optional[str]
    published: datetime
    last_modified: datetime
    base_score: Optional[float]
    identifier: Optional[str]
    status: Optional[str]

    class Config:
        orm_mode = True

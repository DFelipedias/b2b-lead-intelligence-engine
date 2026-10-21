from typing import Optional
from pydantic import BaseModel, HttpUrl

class CompanyLead(BaseModel):
    name: str
    website: str
    industry: str
    description: Optional[str] = None


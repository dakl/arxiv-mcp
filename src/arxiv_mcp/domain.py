from datetime import datetime

from pydantic import BaseModel


class Paper(BaseModel):
    paper_id: str
    title: str
    authors: list[str]
    abstract: str
    published: datetime
    pdf_url: str
    html_url: str

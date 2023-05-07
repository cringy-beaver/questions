from pydantic import BaseModel
from datetime import datetime


class Question(BaseModel):
    id: int
    number: int
    title: str
    body: str
    created_at: datetime
    link_to_s3_question_pic: str | None

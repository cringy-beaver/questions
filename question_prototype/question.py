from pydantic import BaseModel, Field
from datetime import datetime


class Question(BaseModel):
    id: int = Field(..., description="The unique identifier of the question. "
                                     "This is a primary key in the database")
    number: int = Field(..., description="The question number. "
                                         "May not be unique")
    title: str = Field(..., description="The question title")
    body: str = Field(..., description="The question body")
    created_at: datetime = Field(..., description="The date and time "
                                                  "the question was created / "
                                                  "uploaded to the database")
    link_to_s3_question_pic: str | None \
        = Field(..., description="The link to s3. May not be present "
                                 "if no image was uploaded with the question")

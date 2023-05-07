from fastapi import FastAPI, HTTPException
from question_prototype.question import Question
import random
from db_client.ch_client import DBClient

db_client = DBClient(
    host="185.154.194.183",
    port="8123",
    user="master",
    password="content344DB",
)
# TODO use os.getenv to get env variables
# TODO make it async
# TODO create a swagger documentation
app = FastAPI()


@app.post("/questions/")
def create_question(question: Question):
    db_client.add_question(question.dict())
    return {"message": "Question created successfully"}


@app.get("/questions/{question_id}")
def get_questions_by_id(question_id: int):
    questions = db_client.get_questions_filter_by_id(question_id)
    if questions:
        return questions
    raise HTTPException(status_code=404, detail="Question not found")


@app.get("/questions/")
def get_all_questions():
    return db_client.get_all_questions()


@app.get("/questions/random/")
def get_random_question(title: str):
    """Get a random question from the database with specific title"""
    questions = db_client.get_questions_filter_by_title(title)
    if questions:
        return random.choice(questions)
    raise HTTPException(status_code=404, detail="No questions "
                                                "found with this title")


@app.put("/questions/{question_id}")
def update_question(question_id: int, question: Question):
    questions = db_client.get_questions_filter_by_id(question_id)
    for q in questions:
        q.number = question.number
        q.title = question.title
        q.body = question.body
        q.created_at = question.created_at
        q.link_to_s3 = question.link_to_s3_question_pic
        db_client.session.commit()
        return {"message": "Question updated successfully"}
    raise HTTPException(status_code=404, detail="Question not found")


@app.delete("/questions/{question_id}")
def delete_question(question_id: int):
    questions = db_client.get_questions_filter_by_id(question_id)
    for q in questions:
        db_client.session.delete(q)
        db_client.session.commit()
        return {"message": "Question deleted successfully"}
    raise HTTPException(status_code=404, detail="Question not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

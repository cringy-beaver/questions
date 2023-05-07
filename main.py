from fastapi import FastAPI, HTTPException
from question_prototype.question import Question
import random
from db_client.ch_client import DBClient

db_client = DBClient(
    host="185....3",
    port="8123",
    user="hidden",
    password="hidden",
)

app = FastAPI()
# TODO swagger docs
# TODO os.getenv


@app.post("/questions/")
async def create_question(question: Question):
    await db_client.insert_question(question.dict())
    return {"message": "Question created successfully"}


@app.get("/questions/{question_id}")
async def get_questions_by_id(question_id: int):
    questions = await db_client.get_questions_filter_by_id(question_id)
    if questions:
        return questions
    raise HTTPException(status_code=404, detail="Question not found")


@app.get("/questions/")
async def get_all_questions():
    return await db_client.get_all_questions()


@app.get("/questions/random/")
async def get_random_question(title: str):
    """Get a random question from the database with specific title"""
    questions = await db_client.get_questions_filter_by_title(title)
    if questions:
        return random.choice(questions)
    raise HTTPException(status_code=404,
                        detail="No questions found with this title")


@app.put("/questions/{question_id}")
async def update_question(question_id: int, question: Question):
    result = await db_client.update_question(question_id, question.dict())
    if result:
        return {"message": "Question updated successfully"}
    raise HTTPException(status_code=404, detail="Question not found")


@app.delete("/questions/{question_id}")
async def delete_question(question_id: int):
    result = await db_client.delete_question(question_id)
    if result:
        return {"message": "Question deleted successfully"}
    raise HTTPException(status_code=404, detail="Question not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

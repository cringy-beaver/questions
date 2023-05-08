from fastapi import FastAPI, HTTPException
from src.question_prototype.question import Question
from src.db_client.ch_client import DBClient
import random
import uvicorn
import os

db_client = DBClient(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

app = FastAPI()


@app.post("/questions/", description="Creates a question", status_code=200)
async def create_question(question: Question):
    await db_client.insert_question(question.dict())
    return {"message": "Question created successfully"}


@app.get("/questions/{question_id}", description="Get question by id",
         status_code=200)
async def get_questions_by_id(question_id: int):
    questions = await db_client.get_questions_filter_by_id(question_id)
    if questions:
        return questions
    raise HTTPException(status_code=404, detail="Question not found")


@app.get("/questions/", description="Get all questions", status_code=200)
async def get_all_questions():
    return await db_client.get_all_questions()


@app.get("/questions/random/",
         description="Get a random question with specific title",
         status_code=200)
async def get_random_question(title: str):
    """Get a random question from the database with specific title"""
    questions = await db_client.get_questions_filter_by_title(title)
    if questions:
        return random.choice(questions)
    raise HTTPException(status_code=404,
                        detail="No questions found with this title")


@app.put("/questions/{question_id}", description="Update question by id",
         status_code=200)
async def update_question(question_id: int, question: Question):
    result = await db_client.update_question(question_id, question.dict())
    if result:
        return {"message": "Question updated successfully"}
    raise HTTPException(status_code=404, detail="Question not found")


@app.delete("/questions/{question_id}",
            description="Delete question by id",
            status_code=200)
async def delete_question(question_id: int):
    result = await db_client.delete_question(question_id)
    if result:
        return {"message": "Question deleted successfully"}
    raise HTTPException(status_code=404, detail="Question not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

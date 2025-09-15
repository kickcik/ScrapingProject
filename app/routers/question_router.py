import random

from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist

from app.models.questions import Question
from app.models.user_questions import UserQuestion
from app.models.users import User
from app.schemas.question import UserQuestionResponse
from app.utils.auth import get_current_user

question_router = APIRouter(prefix="/questions", tags=["question"])


@question_router.get("/bring", status_code=200)
async def get_question(user: User = Depends(get_current_user)) -> UserQuestionResponse:
    try:
        question_id = random.randint(1, 100)
        question = await Question.get(id=question_id)
        user_question = await UserQuestion.create(question=question, user=user)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Question not found")

    return UserQuestionResponse.model_validate(user_question)

from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: int
    question_text: str

    model_config = {"from_attributes": True}


class UserQuestionResponse(BaseModel):
    id: int
    user_id: int
    question: QuestionResponse

    model_config = {"from_attributes": True}

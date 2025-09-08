from pydantic import BaseModel


class CreateDiaryRequest(BaseModel):
    title: str
    content: str


class UpdateDiaryRequest(BaseModel):
    id: int
    title: str | None = None
    content: str | None = None


class DiaryResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

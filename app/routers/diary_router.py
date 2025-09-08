from sqlite3 import IntegrityError

from fastapi import APIRouter, Depends, HTTPException

from app.models.diaries import Diary
from app.models.users import User
from app.schemas.diaries import CreateDiaryRequest, DiaryResponse, UpdateDiaryRequest
from app.utils.auth import get_current_user

diary_router = APIRouter(prefix="/diaries", tags=["diaries"])


@diary_router.post("/create", status_code=201)
async def create_diary(diary_data: CreateDiaryRequest, user: User = Depends(get_current_user)) -> DiaryResponse:
    try:
        new_diary = await Diary.create(title=diary_data.title, content=diary_data.content, user=user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="invalid diary")
    return DiaryResponse.model_validate(new_diary)


@diary_router.patch("/update", status_code=200)
async def update_diary(diary_data: UpdateDiaryRequest, user: User = Depends(get_current_user)) -> DiaryResponse:
    if not (diary := await Diary.get_or_none(id=diary_data.id)):
        raise HTTPException(status_code=404, detail="invalid diary")
    if diary.user_id != user.id:  # type: ignore[attr-defined]
        raise HTTPException(status_code=403, detail="you are not owner of the diary")

    diary.title = diary_data.title or diary.title
    diary.content = diary_data.content or diary.content
    await diary.save()

    return DiaryResponse.model_validate(diary)


@diary_router.delete("/delete/{diary_id}", status_code=204)
async def delete_diary(diary_id: int, user: User = Depends(get_current_user)) -> None:
    if not (diary := await Diary.get_or_none(id=diary_id)):
        raise HTTPException(status_code=404, detail="invalid diary")
    if diary.user_id != user.id:  # type: ignore[attr-defined]
        raise HTTPException(status_code=403, detail="you are not owner of the diary")

    await diary.delete()

from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.models.bookmarks import Bookmark
from app.models.quotes import Quote
from app.models.users import User
from app.schemas.bookmarks import BookmarkResponse
from app.utils.auth import get_current_user

bookmark_router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])


@bookmark_router.post("/create/{quote_id}", status_code=201)
async def create_bookmark(quote_id: int, user: User = Depends(get_current_user)) -> BookmarkResponse:
    try:
        quote = await Quote.get(id=quote_id)
        bookmark = await Bookmark.create(user=user, quote=quote)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="the bookmark already exists")
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="the quote does not exist")

    return BookmarkResponse.model_validate(bookmark)


@bookmark_router.get("", status_code=200)
async def list_bookmarks(user: User = Depends(get_current_user)) -> list[BookmarkResponse]:
    bookmarks = await Bookmark.filter(user=user).prefetch_related("quote")

    return [BookmarkResponse.model_validate(bookmark) for bookmark in bookmarks]


@bookmark_router.delete("/{bookmark_id}", status_code=204)
async def remove_bookmark(bookmark_id: int, user: User = Depends(get_current_user)) -> None:
    if not (bookmark := await Bookmark.get_or_none(id=bookmark_id)):
        raise HTTPException(status_code=404, detail="the bookmark does not exist")

    await bookmark.delete()

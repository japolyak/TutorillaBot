from fastapi import status, APIRouter

from src.common.models import ItemsDto, TextbookDto

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.contexts.db_contex import DbContext
from src.api.src.contexts.user_context import UserContext
from src.api.src.database.crud.textbook_crud import TextbookCRUD
from src.api.src.routers.api_enpoints import APIEndpoints


router = APIRouter()


@router.get(path=APIEndpoints.Textbook.Get, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[TextbookDto])
async def get_textbooks(tutor_course_id: int, user: UserContext, db: DbContext):
    db_textbooks = TextbookCRUD.get_textbooks(db, tutor_course_id)

    if not db_textbooks:
        return ResponseBuilder.success_response(content=ItemsDto(items=[]))

    textbooks = [TextbookDto(id=t.id, title=t.title) for t in db_textbooks]

    response_model = ItemsDto[TextbookDto](items=textbooks)

    return ResponseBuilder.success_response(content=response_model)


@router.post(path=APIEndpoints.Textbook.Post, status_code=status.HTTP_201_CREATED,
             summary="Creates textbooks")
async def create_textbooks(tutor_course_id: int, new_textbooks: ItemsDto[str], db: DbContext):
    TextbookCRUD.create_textbooks(db, tutor_course_id, new_textbooks.items)

    return ResponseBuilder.success_response(status_code=status.HTTP_201_CREATED)



@router.delete(path=APIEndpoints.Textbook.Delete, status_code=status.HTTP_204_NO_CONTENT,
               summary="Deletes textbook")
async def delete_textbook(textbook_id: int, db: DbContext):
    deletion = TextbookCRUD.delete_textbook(db, textbook_id)

    if not deletion:
        return ResponseBuilder.error_response(message='Textbook was not found')

    return ResponseBuilder.success_response(status_code=status.HTTP_204_NO_CONTENT)

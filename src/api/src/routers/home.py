from fastapi import APIRouter

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.routers.api_enpoints import APIEndpoints


router = APIRouter()


@router.get(APIEndpoints.Home.Get)
async def root():
    # return ResponseBuilder.error_response(message="Test")
    return ResponseBuilder.success_response(content={"message": f"Welcome home!"})

    # return {"message": f"Welcome home!"}

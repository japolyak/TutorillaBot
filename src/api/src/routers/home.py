from fastapi import APIRouter

from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.routers.api_enpoints import APIEndpoints


router = APIRouter()


@router.get(APIEndpoints.Home.Get)
async def root():
    return ResponseBuilder.success_response(content={"message": f"Welcome home!"})

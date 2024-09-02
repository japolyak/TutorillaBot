from requests import Response
from typing import Generic, Type, Optional


from src.common.models import T, ErrorDto


class ApiResponse(Generic[T]):
    def __init__(self, data: Optional[T] = None, error: Optional[ErrorDto] = None):
        self.success = data is not None
        self.data = data
        self.error = error

    def is_successful(self) -> bool:
        return self.success


class ApiUtils:
    @staticmethod
    def create_api_response(response: Response, model_class: Type[T]) -> ApiResponse[T]:
        if not response.ok:
            error = ErrorDto(**response.json())
            return ApiResponse[T](error=error)

        json_data = response.json()
        data = model_class(**json_data)

        return ApiResponse[T](data=data)

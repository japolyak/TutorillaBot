from fastapi import APIRouter

from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.routers.admin import router as admin_router
from src.api.src.routers.home import router as home_router
from src.api.src.routers.private_course import router as private_course_router
from src.api.src.routers.subject import router as subject_router
from src.api.src.routers.tutor_course import router as tutor_course_router
from src.api.src.routers.user import router as user_router
from src.api.src.routers.authentication import router as authentication_router
from src.api.src.routers.textbook import router as textbook_router
from src.api.src.routers.event import router as event_router


api_router = APIRouter()

api_router.include_router(admin_router, prefix=APIEndpoints.Admin.Prefix, tags=["admin"])
api_router.include_router(home_router, prefix=APIEndpoints.Home.Prefix, tags=["home"])
api_router.include_router(private_course_router, prefix=APIEndpoints.PrivateCourses.Prefix, tags=["private-courses"])
api_router.include_router(subject_router, prefix=APIEndpoints.Subjects.Prefix, tags=["subjects"])
api_router.include_router(tutor_course_router, prefix=APIEndpoints.TutorCourse.Prefix, tags=["tutor-courses"])
api_router.include_router(user_router, prefix=APIEndpoints.Users.Prefix, tags=["users"])
api_router.include_router(authentication_router, prefix=APIEndpoints.Authentication.Prefix, tags=["authentication"])
api_router.include_router(textbook_router, prefix=APIEndpoints.Textbook.Prefix, tags=["textbooks"])
api_router.include_router(event_router, prefix=APIEndpoints.Events.Prefix, tags=["events"])

from fastapi import status, APIRouter
import time
from operator import itemgetter

from src.common.models import ScheduleEventDto, NewClassDto, ItemsDto, ScheduleEventType, Role

from src.api.src.bot_client.message_sender import send_notification_about_new_class
from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.contexts.db_contex import DbContext
from src.api.src.contexts.user_context import UserContext
from src.api.src.database.crud.events_crud import EventCRUD
from src.api.src.database.crud.private_courses_crud import PrivateCourseCRUD
from src.api.src.functions.time_transformator import transform_class_time
from src.api.src.routers.api_enpoints import APIEndpoints


router = APIRouter()


@router.get(path=APIEndpoints.Events.Range, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[ScheduleEventDto])
async def get_events_in_range(start: int, end: int, user: UserContext, db: DbContext):
    if user.role not in [Role.Tutor, Role.Student]:
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    db_events = EventCRUD.get_events_between_dates(user.id, user.role, start, end, db)

    events = [
        ScheduleEventDto(
            id=event[0],
            duration=event[1],
            date=event[2],
            type=ScheduleEventType.Class,
            subject_name=event[3],
            person_name=event[4]
        )
        for event in db_events
    ]

    return ResponseBuilder.success_response(content=ItemsDto[ScheduleEventDto](items=events))


@router.post(path=APIEndpoints.Events.CreateClass, status_code=status.HTTP_201_CREATED,
             summary="Add new class for private course")
async def add_new_class(private_course_id: int, new_class: NewClassDto, user: UserContext, db: DbContext):
    if user.role not in [Role.Tutor, Role.Student]:
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    current_timestamp = int(time.time()) * 1000

    if current_timestamp > new_class.time:
        return ResponseBuilder.error_response(message="Not before now!")

    private_course_info = PrivateCourseCRUD.get_private_course_info(private_course_id, db)

    if private_course_info is None:
        return ResponseBuilder.error_response(message="Course does not exist!")

    has_collisions = EventCRUD.event_has_collisions(db, private_course_id, new_class.time, new_class.duration)

    if has_collisions:
        return ResponseBuilder.error_response(message="Class has collisions!")

    EventCRUD.create_class_event(db, private_course_id, new_class.time, new_class.duration)

    if user.role is Role.Tutor:
        subject, sender_name, recipient_id, recipient_timezone = itemgetter(0, 5, 1, 3)(private_course_info)
    else:
        subject, sender_name, recipient_id, recipient_timezone = itemgetter(0, 2, 4, 6)(private_course_info)

    class_date = transform_class_time(new_class.time, recipient_timezone)

    send_notification_about_new_class(recipient_id, sender_name, subject, class_date)

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)

from fastapi import status, APIRouter
import time

from src.common.models import ScheduleEventDto, NewClassDto, ItemsDto, ScheduleEventType

from src.api.src.bot_client.message_sender import send_notification_about_new_class
from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.database.crud.events_crud import EventCRUD
from src.api.src.database.db_setup import DbContext
from src.api.src.functions.time_transformator import transform_class_time
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.utils.token_utils import UserContext


router = APIRouter()


@router.get(path=APIEndpoints.Events.Range, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[ScheduleEventDto])
async def get_events_in_range(start: int, end: int, user: UserContext, db: DbContext):
    db_events = EventCRUD.get_events_between_dates(db, user.id, user.role, start, end)

    events = [
        ScheduleEventDto(
            id=event.id,
            duration=event.duration,
            date=event.start_time_unix,
            type=ScheduleEventType.Class,
            title=f'Class - {event.id}'
        )
        for event in db_events
    ]

    return ResponseBuilder.success_response(content=ItemsDto[ScheduleEventDto](items=events))


@router.post(path=APIEndpoints.Events.CreateClass, status_code=status.HTTP_201_CREATED,
             summary="Add new class for private course")
async def add_new_class(private_course_id: int, new_class: NewClassDto, user: UserContext, db: DbContext):
    schedule = new_class.time
    current_timestamp = int(time.time())

    if current_timestamp > (schedule / 1000):
        return ResponseBuilder.error_response(message="Not before now!")

    EventCRUD.create_class_event(db, private_course_id, new_class.time, new_class.duration)

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)
    # TODO - reimplement after token implementation

    if error_msg:
        return ResponseBuilder.error_response(message=error_msg)

    class_date = transform_class_time(schedule, recipient_timezone).strftime('%H:%M %d-%m-%Y')

    send_notification_about_new_class(recipient_id, sender_name, subject_name, class_date)

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)

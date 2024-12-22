from fastapi import status, APIRouter
import time
from operator import itemgetter

from src.core.models import ScheduleEventDto, NewClassDto, ItemsDto, ScheduleEventType, Role

from src.api.src.bot_client.message_sender import MessageSender
from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.contexts.db_contex import DbContext
from src.api.src.contexts.user_context import UserContext
from src.api.src.database.crud.events_crud import EventCRUD
from src.api.src.database.crud.private_courses_crud import PrivateCourseCRUD
from src.api.src.functions.time_transformator import transform_class_time
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.validators.event_validator import EventValidator


router = APIRouter()


@router.get(path=APIEndpoints.Events.Range, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[ScheduleEventDto])
async def get_events_in_range(start: int, end: int, user: UserContext, db: DbContext):
    if not user.has_any_role((Role.Tutor, Role.Student)):
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    role = Role.Student if user.has_role(Role.Student) else Role.Tutor

    db_events = EventCRUD.get_events_between_dates(user.id, role, start, end, db)

    events = [
        ScheduleEventDto(
            id=event[0],
            duration=event[1],
            date=event[2],
            type=ScheduleEventType.Class,
            subject_name=event[3],
            person_name=event[4],
            person_timezone=event[5],
            private_course_id=event[6]
        )
        for event in db_events
    ]

    return ResponseBuilder.success_response(content=ItemsDto[ScheduleEventDto](items=events))


@router.post(path=APIEndpoints.Events.CreateClass, status_code=status.HTTP_201_CREATED,
             summary="Add new class for private course")
async def add_new_class(private_course_id: int, new_class: NewClassDto, user: UserContext, db: DbContext):
    if not user.has_any_role((Role.Tutor, Role.Student)):
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    current_timestamp = int(time.time()) * 1000

    if current_timestamp > new_class.time:
        return ResponseBuilder.error_response(message="Not before now!")

    private_course_info = PrivateCourseCRUD.get_private_course_info(private_course_id, db)

    if private_course_info is None:
        return ResponseBuilder.error_response(message="Course does not exist!")

    student_id, tutor_id = itemgetter(1, 4)(private_course_info)

    has_collisions = EventCRUD.event_has_collisions(student_id, tutor_id, new_class.time, new_class.duration, None, db)

    if has_collisions:
        return ResponseBuilder.error_response(message="Class has collisions!")

    EventCRUD.create_class_event(db, private_course_id, new_class.time, new_class.duration)

    if user.has_role(Role.Tutor):
        recipient_id = student_id
        subject, sender_name, recipient_timezone = itemgetter(0, 5, 3)(private_course_info)
    else:
        recipient_id = tutor_id
        subject, sender_name, recipient_timezone = itemgetter(0, 2, 6)(private_course_info)

    class_date = transform_class_time(new_class.time, recipient_timezone)

    MessageSender.send_notification_about_new_class(recipient_id, sender_name, subject, class_date)

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)


@router.delete(path=APIEndpoints.Events.Delete, status_code=status.HTTP_204_NO_CONTENT,
             summary="Delete class for private course")
async def delete_class(event_id: int, user: UserContext, db: DbContext):
    if not user.has_any_role((Role.Tutor, Role.Student)):
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    validation = EventValidator(user, db).delete_event(event_id)

    if not validation.is_valid:
        return ResponseBuilder.error_response(message=validation.errors[0])

    event_deleted = EventCRUD.delete_event(event_id, db)

    if not event_deleted:
        return ResponseBuilder.error_response(message="Something went wrong. Please try later.")

    return ResponseBuilder.success_response(status.HTTP_204_NO_CONTENT)


@router.patch(path=APIEndpoints.Events.Patch, status_code=status.HTTP_204_NO_CONTENT,
             summary="Update class for private course")
async def update_class(event_id: int, new_class: NewClassDto, user: UserContext, db: DbContext):
    if not user.has_any_role((Role.Tutor, Role.Student)):
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    current_timestamp = int(time.time()) * 1000

    if current_timestamp > new_class.time:
        return ResponseBuilder.error_response(message="Not before now!")

    event = EventCRUD.get_event(event_id, db)

    if not event:
        return ResponseBuilder.error_response(message="Event does not exist!")

    if event.has_occurred or event.is_paid:
        return ResponseBuilder.error_response(message="Event has occurred!")

    members = PrivateCourseCRUD.get_private_course_members(event.private_course_id, db)

    if not members: return ResponseBuilder.error_response(message="Private course does not exist!")

    student_id, tutor_id = itemgetter(0, 1)(members)

    has_collisions = EventCRUD.event_has_collisions(student_id, tutor_id, new_class.time, new_class.duration, event_id, db)

    if has_collisions:
        return ResponseBuilder.error_response(message="Class has collisions!")

    EventCRUD.update_class_event(event_id, new_class.time, new_class.duration, db)

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)
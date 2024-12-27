from fastapi import status, APIRouter
import time
from operator import itemgetter

from src.api.src.bot_client.message_sender import MessageSender
from src.api.src.builders.response_builder import ResponseBuilder
from src.api.src.contexts.db_contex import DbContext
from src.api.src.contexts.user_context import UserContext
from src.api.src.database.crud.events_crud import EventCRUD
from src.api.src.database.crud.private_courses_crud import PrivateCourseCRUD
from src.api.src.routers.api_enpoints import APIEndpoints
from src.api.src.validators.event_validator import EventValidator

from src.core.models import ScheduleEventDto, NewClassDto, ItemsDto, ScheduleEventType, Role


router = APIRouter()


@router.get(path=APIEndpoints.Events.Range, status_code=status.HTTP_200_OK,
            response_model=ItemsDto[ScheduleEventDto])
async def get_events_in_range(start: int, end: int, user: UserContext, db: DbContext):
    if not user.has_any_role((Role.Tutor, Role.Student)):
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    role = Role.Student if user.has_role(Role.Student) else Role.Tutor

    db_events = EventCRUD.get_events_between_dates(user.id, role, start, end, db)

    events = [ScheduleEventDto.from_tuple(event, ScheduleEventType.Class) for event in db_events]

    return ResponseBuilder.success_response(content=ItemsDto[ScheduleEventDto](items=events))


@router.post(path=APIEndpoints.Events.CreateClass, status_code=status.HTTP_201_CREATED,
             summary="Add new class for private course")
async def add_new_event(private_course_id: int, new_class: NewClassDto, user: UserContext, db: DbContext):
    if not user.has_any_role((Role.Tutor, Role.Student)):
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    current_timestamp = int(time.time()) * 1000

    if current_timestamp > new_class.time:
        return ResponseBuilder.error_response(message="Not before now!")

    private_course_info = PrivateCourseCRUD.get_private_course_info(private_course_id, db)

    if private_course_info is None:
        return ResponseBuilder.error_response(message="Course does not exist!")

    student_id, tutor_id = itemgetter(1, 3)(private_course_info)

    has_collisions = EventCRUD.event_has_collisions(student_id, tutor_id, new_class.time, new_class.duration, None, db)

    if has_collisions:
        return ResponseBuilder.error_response(message="Class has collisions!")

    event = EventCRUD.create_class_event(db, private_course_id, new_class.time, new_class.duration)

    sender_name_pointer = 4 if user.has_role(Role.Tutor) else 2
    recipient_id = student_id if user.has_role(Role.Tutor) else tutor_id

    subject, sender_name = itemgetter(0, sender_name_pointer)(private_course_info)

    MessageSender.send_notification_about_new_class(recipient_id, sender_name, subject, event.id)

    return ResponseBuilder.success_response(status.HTTP_201_CREATED)


@router.delete(path=APIEndpoints.Events.Delete, status_code=status.HTTP_204_NO_CONTENT,
             summary="Delete class for private course")
async def delete_event(event_id: int, user: UserContext, db: DbContext):
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
async def update_event(event_id: int, new_class: NewClassDto, user: UserContext, db: DbContext):
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


@router.get(path=APIEndpoints.Events.Get, status_code=status.HTTP_200_OK, response_model=ScheduleEventDto)
async def get_event(event_id: int, user: UserContext, db: DbContext):
    if not user.has_any_role((Role.Tutor, Role.Student)):
        return ResponseBuilder.error_response(status.HTTP_403_FORBIDDEN, message="Access denied!")

    role = Role.Student if user.has_role(Role.Student) else Role.Tutor

    db_event = EventCRUD.get_event_with_details(user.id, event_id, role, db)

    if not db_event:
        return ResponseBuilder.error_response(message="Event does not exist!")

    members = PrivateCourseCRUD.get_private_course_members(db_event[6], db)

    if not members: return ResponseBuilder.error_response(message="Private course does not exist!")

    student_id, tutor_id = itemgetter(0, 1)(members)

    if user.has_role(Role.Tutor):
        if tutor_id != user.id:
            return ResponseBuilder.error_response(message="You are not the tutor of the current course!")
    else:
        if student_id != user.id:
            return ResponseBuilder.error_response(message="You are not the student of the current course!")

    event = ScheduleEventDto.from_tuple(db_event, ScheduleEventType.Class)

    return ResponseBuilder.success_response(content=event)

from operator import itemgetter

from src.api.src.database.crud.events_crud import EventCRUD
from src.api.src.database.crud.private_courses_crud import PrivateCourseCRUD
from src.api.src.validators.i_validator import IValidator

from src.core.models import Role


class EventValidator(IValidator):
    def delete_event(self, event_id: int):
        event = EventCRUD.get_event(event_id, self._db)

        if not event:
            self._errors.append("Event does not exist!")

        if not event.is_scheduled or event.has_occurred or event.is_paid:
            self._errors.append("Event has occurred!")
            return self

        members = PrivateCourseCRUD.get_private_course_members(event.private_course_id, self._db)

        if not members:
            self._errors.append("Private course does not exist!")
            return self

        student_id, tutor_id = itemgetter(0, 1)(members)

        if self._user.has_role(Role.Tutor):
            if tutor_id != self._user.id:
                self._errors.append("You are not the tutor of the current course!")
        else:
            if student_id != self._user.id:
                self._errors.append("You are not the student of the current course!")

        return self

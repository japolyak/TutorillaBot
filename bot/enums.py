from enum import Enum, StrEnum


class CallBackPrefix(StrEnum):
    SetFirstName = "set_first_name"
    SetLastName = "set_last_name"
    SetPhone = "set_phone"
    SetEmail = "set_email"
    BecomeTutor = "become_tutor"
    BecomeStudent = "become_student"
    AddCourse = "add_course"
    SubscribeCourse = "subscribe_course"
    ReturnToSelect = "return_to_select"
    TutorCourseClasses = "tutor_course_classes"
    InvoicesForTutor = "invoices_for_tutor"
    BackToPrivateCourse = "Back_to_private_course"
    BackToChoosePrivateCourse = "back_to_choose_private_course"
    PrivateClass = "private_class"
    RoleRequest = "role_request"
    BackToAdminPanel = "back_to_admin_panel"
    AcceptRole = "accept_role"
    DeclineRole = "decline_role"
    BackToUsersRequests = "back_to_users_requests"


class Emoji(Enum):
    ClassScheduled = u'\U0001F4C5'
    ClassOccurred = u'\U00002705'
    ClassPaid = u'\U0001F4B0'
    BackArrow = u'\u2B05'
    Accept = u'\u2714'
    Decline = u'\u274C'


class Role(StrEnum):
    Tutor = "tutor"
    Student = "student"
    Admin = "admin"

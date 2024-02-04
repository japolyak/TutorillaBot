from typing import Literal
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from bot.i18n.i18n import t
from ..api.api_models import *
from ..config import web_app_link
from ..enums import *


class InlineKeyboardMarkupCreator:
    @staticmethod
    def language_markup(command: str) -> InlineKeyboardMarkup:
        ukr_btn = InlineKeyboardButton("Українська", callback_data=f"{command} ua")
        rus_btn = InlineKeyboardButton("Русский", callback_data=f"{command} ru")
        eng_btn = InlineKeyboardButton("English", callback_data=f"{command} en")
        pol_btn = InlineKeyboardButton("Polski", callback_data=f"{command} pl")

        markup = InlineKeyboardMarkup([[ukr_btn, rus_btn, eng_btn], [pol_btn]])

        return markup

    @staticmethod
    def change_profile(language: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        first_name_btn = InlineKeyboardButton(t(language, "first_name"), callback_data=CallBackPrefix.SetFirstName)
        last_name_btn = InlineKeyboardButton(t(language, "last_name"), callback_data=CallBackPrefix.SetLastName)
        phone_btn = InlineKeyboardButton(t(language, "phone"), callback_data=CallBackPrefix.SetPhone)
        email_btn = InlineKeyboardButton(t(language, "email"), callback_data=CallBackPrefix.SetEmail)

        markup.add(first_name_btn, last_name_btn).add(phone_btn, email_btn)

        return markup

    @staticmethod
    def choose_occupation() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        teacher_btn = InlineKeyboardButton("Teach", callback_data=CallBackPrefix.BecomeTutor)
        student_btn = InlineKeyboardButton("Study", callback_data=CallBackPrefix.BecomeStudent)

        markup.add(teacher_btn, student_btn)

        return markup

    @staticmethod
    def tutor_courses_markup(courses: List[SubjectDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Tutor {course.name}"))
            for course
            in courses]

        return markup

    @staticmethod
    def student_courses_markup(courses: List[SubjectDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Student {course.name}"))
            for course
            in courses]

        return markup

    @staticmethod
    def add_course_markup(courses: List[SubjectDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, callback_data=f"{CallBackPrefix.AddCourse} {course.id}"))
            for course
            in courses]

        return markup

    @staticmethod
    def sub_course_markup(courses: List[SubjectDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Subscribe {course.name}"))
            for course
            in courses]

        return markup

    @staticmethod
    def subscribe_course_markup(course_id: int) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        subscribe_btn = InlineKeyboardButton("Subscribe", callback_data=f"SubscribeCourse {course_id}")
        return_btn = InlineKeyboardButton("Return to select subjects", callback_data="ReturnToSelect")

        markup.add(subscribe_btn).add(return_btn)

        return markup

    @staticmethod
    def tutor_student_course_markup(private_course: PrivateCourseDto, role: Literal["tutor", "student"]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        plan_class_btn = InlineKeyboardButton("Plan class",
                                              web_app=WebAppInfo(
                                                  url=f"{web_app_link}/tutor/private-course/{private_course.id}"
                                              ))
        all_classes_btn = InlineKeyboardButton("All classes", callback_data=f"{CallBackPrefix.CourseClasses} {private_course.id} {role}")
        # invoices_btn = InlineKeyboardButton("Invoices", callback_data=CallBackPrefix.InvoicesForTutor)
        back_btn = InlineKeyboardButton("Back", callback_data=CallBackPrefix.BackToChoosePrivateCourse)

        markup.add(plan_class_btn).add(all_classes_btn).add(back_btn)

        return markup

    @staticmethod
    def course_classes_markup(private_class: PrivateClassDto) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=f"{Emoji.ClassPaid.value if i.is_paid else (Emoji.ClassOccurred.value if i.has_occurred else Emoji.ClassScheduled.value)} {i.schedule_datetime.strftime("%d-%m-%Y %H:%M")}",
                                 callback_data=f"{CallBackPrefix.PrivateClass} {i.id}")
        )
            for i
            in private_class.classes]

        markup.add(
            InlineKeyboardButton(text=f"{Emoji.BackArrow.value} Back to course",
                                 callback_data=f"{CallBackPrefix.BackToPrivateCourse} {private_class.private_course.id}"
                                 )
        )

        return markup

    @staticmethod
    def requests_markup(requests: list[UserRequestDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=f"{i.id}", callback_data=f"{CallBackPrefix.RoleRequest} {i.id}")
        ) for i in requests]

        return markup

    @staticmethod
    def request_decision_markup(user_id: int, role: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        accept_btn = InlineKeyboardButton(text=f"{Emoji.Accept.value} Accept",
                                          callback_data=f"{CallBackPrefix.AcceptRole} {user_id} {role}")
        decline_btn = InlineKeyboardButton(text=f"{Emoji.Decline.value} Decline",
                                           callback_data=f"{CallBackPrefix.DeclineRole} {user_id}")
        back_to_requests = InlineKeyboardButton(text=f"{Emoji.BackArrow.value} Back",
                                                callback_data=f"{CallBackPrefix.BackToUsersRequests} {role}")

        markup.add(accept_btn).add(decline_btn).add(back_to_requests)

        return markup

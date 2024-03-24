from typing import Literal
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from bot.i18n.i18n import t
from ..api.api_models import *
from ..config import web_app_link
from ..enums import *
from telebot import service_utils


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

        # first_name_btn = InlineKeyboardButton(t(language, "first_name"), callback_data=CallBackPrefix.SetFirstName)
        # last_name_btn = InlineKeyboardButton(t(language, "last_name"), callback_data=CallBackPrefix.SetLastName)
        # phone_btn = InlineKeyboardButton(t(language, "phone"), callback_data=CallBackPrefix.SetPhone)
        # email_btn = InlineKeyboardButton(t(language, "email"), callback_data=CallBackPrefix.SetEmail)

        # markup.add(first_name_btn, last_name_btn).add(phone_btn, email_btn)

        return markup

    @staticmethod
    def choose_occupation() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        teacher_btn = InlineKeyboardButton("Teach", callback_data=CallBackPrefix.BecomeTutor)
        student_btn = InlineKeyboardButton("Study", callback_data=CallBackPrefix.BecomeStudent)

        markup.add(teacher_btn, student_btn)

        return markup

    @staticmethod
    def subjects_markup(courses: List[SubjectDto], role: Literal["Tutor", "Student"]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"{role} {course.name}"))
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

        subscribe_btn = InlineKeyboardButton("Subscribe", callback_data=f"{CallBackPrefix.SubscribeCourse} {course_id}")
        return_btn = InlineKeyboardButton("Return to select subjects", callback_data="ReturnToSelect")

        markup.add(subscribe_btn).add(return_btn)

        return markup

    @staticmethod
    def private_course_markup(private_course_id: int, role: Literal["tutor", "student"]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        plan_class_btn = InlineKeyboardButton("Plan class",
                                              web_app=WebAppInfo(
                                                  url=f"{web_app_link}"
                                              ))
        all_classes_btn = InlineKeyboardButton("All classes", callback_data=f"{CallBackPrefix.CourseClasses} {private_course_id} {role}")
        back_btn = InlineKeyboardButton("Back", callback_data=f"{CallBackPrefix.BackToChoosePrivateCourse} {role}")

        markup.add(plan_class_btn).add(all_classes_btn).add(back_btn)

        return markup

    @staticmethod
    def course_classes_markup(paginated_list: PaginatedList[PrivateClassBaseDto], go_back_id: int, role: str, inline_message_id: str) -> InlineKeyboardMarkup:
        markup = CustomInlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=f"{Emoji.ClassPaid.value if i.is_paid else (Emoji.ClassOccurred.value if i.has_occurred else Emoji.ClassScheduled.value)} {i.schedule_datetime.strftime("%d-%m-%Y %H:%M")}",
                                 callback_data=f"{CallBackPrefix.PrivateClass} {i.id}")
        )
            for i
            in paginated_list.items]

        row = [
            InlineKeyboardButton(text=f"{Emoji.BackArrow.value}",
                                 callback_data=f"{CallBackPrefix.LoadPage} {paginated_list.current_page - 1} {go_back_id} {role} {inline_message_id}"if paginated_list.current_page > 1 else CallBackPrefix.EmptyCallback),
            InlineKeyboardButton(text=f"{paginated_list.current_page}/{paginated_list.pages}",
                                 callback_data=CallBackPrefix.EmptyCallback),
            InlineKeyboardButton(text=f"{Emoji.NextArrow.value}",
                                 callback_data=f"{CallBackPrefix.LoadPage} {paginated_list.current_page + 1} {go_back_id} {role} {inline_message_id}" if paginated_list.current_page < paginated_list.pages else CallBackPrefix.EmptyCallback),
        ]

        markup.add_row(row)

        markup.add(
            InlineKeyboardButton(text=f"{Emoji.BackArrow.value} Back to course",
                                 callback_data=f"{CallBackPrefix.BackToPrivateCourse} {go_back_id} {inline_message_id} {role}"
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


class CustomInlineKeyboardMarkup(InlineKeyboardMarkup):
    def add_row(self, buttons: List[InlineKeyboardButton], row_width=None):
        if row_width is None:
            row_width = self.row_width

        for row in service_utils.chunks(buttons, row_width):
            button_array = [button for button in row]
            self.keyboard.append(button_array)

        return self

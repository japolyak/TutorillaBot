from typing import Literal, List
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from bot.api.api_models import PaginatedList, PrivateClassBaseDto, SubjectDto, UserRequestDto, Role
from bot.config import web_app_link
from bot.enums import Emoji
from bot.handlers.callback_query_handler.callback_prefix import CallBackPrefix
from telebot import service_utils
from bot.i18n.i18n import t


class InlineKeyboardMarkupCreator:
    @staticmethod
    def locale_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        english = InlineKeyboardButton("English", callback_data=f"{CallBackPrefix.SetUserLocale} en-US")

        markup.add(english)

        return markup

    @staticmethod
    def timezone_markup(locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        plus_one = InlineKeyboardButton("Central Europe - Warsaw, Paris, Barcelona", callback_data=f"{CallBackPrefix.SetTimeZone} 2 {locale}")
        plus_two = InlineKeyboardButton("East Europe - Kyiv, Bucharest, Helsinki", callback_data=f"{CallBackPrefix.SetTimeZone} 3 {locale}")

        markup.add(plus_one)
        markup.add(plus_two)

        return markup

    @staticmethod
    def choose_occupation(user_id: int, locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        teacher_btn = InlineKeyboardButton(text=t(user_id, "TeachIKBtn", locale), callback_data=f"{CallBackPrefix.BecomeTutor} {locale}")
        student_btn = InlineKeyboardButton(text=t(user_id, "StudyIKBtn", locale), callback_data=f"{CallBackPrefix.BecomeStudent} {locale}")

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
    def add_course_markup(courses: List[SubjectDto], locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, callback_data=f"{CallBackPrefix.AddCourse} {course.id} {course.name} {locale}"))
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
    def subscribe_course_markup(course_id: int, user_id: int, locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        subscribe_btn = InlineKeyboardButton(text=t(user_id, "SubscribeIKBtn", locale),
                                             callback_data=f"{CallBackPrefix.SubscribeCourse} {course_id} {locale}")
        return_btn = InlineKeyboardButton(text=t(user_id, "ReturnToSelectSubjectsIKBtn", locale),
                                          callback_data=f"{CallBackPrefix.ReturnToSelect} {locale}")

        markup.add(subscribe_btn).add(return_btn)

        return markup

    @staticmethod
    def private_course_markup(private_course_id: int, role: Literal[Role.Tutor, Role.Student], locale, user_id: int) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        # TODO - think about adding role to an url
        plan_class_btn = InlineKeyboardButton(text=t(user_id, "PlanClassIKBtn", locale),
                                              web_app=WebAppInfo(
                                                  url=f"{web_app_link}/private-course/{private_course_id}"
                                              ))

        all_classes_btn = InlineKeyboardButton(text=t(user_id, "AllClassesIKBtn", locale),
                                               callback_data=f"{CallBackPrefix.CourseClasses} {private_course_id} {role} {locale}")
        back_btn = InlineKeyboardButton(text=t(user_id, "BackIKBtn", locale),
                                        callback_data=f"{CallBackPrefix.BackToChoosePrivateCourse} {role} {locale}")

        markup.add(plan_class_btn).add(all_classes_btn).add(back_btn)

        return markup

    @staticmethod
    def test_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        test_btn = InlineKeyboardButton("Test", callback_data="Test")
        back_btn = InlineKeyboardButton("Back", callback_data="Back")

        markup.add(test_btn).add(back_btn)

        return markup

    @staticmethod
    def course_classes_markup(paginated_list: PaginatedList[PrivateClassBaseDto], go_back_id: int, role: str,
                              inline_message_id: str, locale: str, user_id: int) -> InlineKeyboardMarkup:
        markup = CustomInlineKeyboardMarkup()

        for i in paginated_list.items:
            callback_data = f"{CallBackPrefix.PrivateClass} {i.id} {locale}"

            markup.add(
                InlineKeyboardButton(
                    text=f"{Emoji.ClassPaid.value if i.is_paid else (Emoji.ClassOccurred.value if i.has_occurred else Emoji.ClassScheduled.value)} {i.schedule_datetime.strftime("%d-%m-%Y %H:%M")}",
                    callback_data=callback_data)
            )

        back_btn_text = f"{Emoji.BackArrow.value}"
        current_btn_text = f"{paginated_list.current_page}/{paginated_list.pages}"
        next_btn_text = f"{Emoji.NextArrow.value}"

        back_btn_callback = f"{CallBackPrefix.LoadPage} {paginated_list.current_page - 1} {go_back_id} {role} {inline_message_id} {locale}"if paginated_list.current_page > 1 else CallBackPrefix.EmptyCallback
        current_btn_callback = CallBackPrefix.EmptyCallback
        next_btn_callback = f"{CallBackPrefix.LoadPage} {paginated_list.current_page + 1} {go_back_id} {role} {inline_message_id} {locale}" if paginated_list.current_page < paginated_list.pages else CallBackPrefix.EmptyCallback

        row = [
            InlineKeyboardButton(text=back_btn_text, callback_data=back_btn_callback),
            InlineKeyboardButton(text=current_btn_text, callback_data=current_btn_callback),
            InlineKeyboardButton(text=next_btn_text, callback_data=next_btn_callback),
        ]

        markup.add_row(row)

        back_to_course_btn_callback = f"{CallBackPrefix.BackToPrivateCourse} {go_back_id} {inline_message_id} {role} {locale}"

        markup.add(
            InlineKeyboardButton(text=f"{Emoji.BackArrow.value} {t(user_id, "BackToCourseIKBtn", locale)}",
                                 callback_data=back_to_course_btn_callback
                                 )
        )

        return markup

    @staticmethod
    def requests_markup(requests: list[UserRequestDto], locale) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=f"{i.id}", callback_data=f"{CallBackPrefix.RoleRequest} {i.id} {locale}")
        ) for i in requests]

        return markup

    @staticmethod
    def request_decision_markup(user_id: int, role: str, locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        accept_btn = InlineKeyboardButton(text=f"{Emoji.Accept.value} {t(user_id, "AcceptIKBtn", locale)}",
                                          callback_data=f"{CallBackPrefix.AcceptRole} {user_id} {role} {locale}")
        decline_btn = InlineKeyboardButton(text=f"{Emoji.Decline.value} {t(user_id, "DeclineIKBtn", locale)}",
                                           callback_data=f"{CallBackPrefix.DeclineRole} {user_id} {locale}")
        back_to_requests = InlineKeyboardButton(text=f"{Emoji.BackArrow.value} {t(user_id, "BackToCourseIKBtn", locale)}",
                                                callback_data=f"{CallBackPrefix.BackToUsersRequests} {role} {locale}")

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

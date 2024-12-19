from telebot import service_utils
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from typing import Literal, List, Optional

from src.core.config import web_app_link
from src.core.models import SubjectDto, Role, BlaTutorCourseDto
from src.core.bot.enums import CallBackPrefix, InlineQueryParam
from src.core.i18n.i18n import t


class InlineKeyboardMarkupCreator:
    @staticmethod
    def admin_panel(user_id: int, locale: Optional[str], *args, **kwargs) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        requests = InlineKeyboardButton(text=t(user_id, "UsersRequestsIKBtn", locale),
                                        web_app=WebAppInfo(url=f"{web_app_link}/admin-panel/requests"))
        markup.add(requests)

        return markup

    @staticmethod
    def classroom_markup(user_id: int, locale: Optional[str], *args, **kwargs) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        schedule = InlineKeyboardButton(text=t(user_id, "ScheduleIKBtn", locale),
                                        web_app=WebAppInfo(url=f"{web_app_link}/schedule"))
        markup.add(schedule)

        if kwargs["is_student"]:
            find_course = InlineKeyboardButton(text=t(user_id, "FindTutorIKBtn", locale),
                                               callback_data=f"{CallBackPrefix.FindTutor} {locale}")
            markup.add(find_course)

        return markup

    @staticmethod
    def locale_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        english = InlineKeyboardButton("English", callback_data=f"{CallBackPrefix.SetUserLocale} en-US")

        markup.add(english)

        return markup

    @staticmethod
    def timezone_markup(locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        plus_one = InlineKeyboardButton("Central Europe - Warsaw, Paris, Barcelona",
                                        callback_data=f"{CallBackPrefix.SetTimeZone} 2 {locale}")
        plus_two = InlineKeyboardButton("East Europe - Kyiv, Bucharest, Helsinki",
                                        callback_data=f"{CallBackPrefix.SetTimeZone} 3 {locale}")

        markup.add(plus_one)
        markup.add(plus_two)

        return markup

    @staticmethod
    def choose_occupation(user_id: int, locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        teacher_btn = InlineKeyboardButton(text=t(user_id, "TeachIKBtn", locale),
                                           callback_data=f"{CallBackPrefix.BecomeTutor} {locale}")
        student_btn = InlineKeyboardButton(text=t(user_id, "StudyIKBtn", locale),
                                           callback_data=f"{CallBackPrefix.BecomeStudent} {locale}")

        markup.add(teacher_btn, student_btn)

        return markup

    @staticmethod
    def subjects_panel_markup(courses: List[BlaTutorCourseDto], user_id: int, locale: str) -> InlineKeyboardMarkup:
        # TODO - rewrite with paging
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=f"{c.subject_name} - {c.price}$",
                                 callback_data=f"{CallBackPrefix.GetTutorCoursesForPanel} {c.id} {locale}"))
            for c
            in courses]

        markup.add(InlineKeyboardButton(text=t(user_id, "ReturnToOfficeIKBtn", locale),
                                        callback_data=f"{CallBackPrefix.BackToOffice} {locale}"))

        return markup

    @staticmethod
    def subjects_markup(subjects: List[SubjectDto], role: Literal[Role.Tutor, Role.Student], query_param: InlineQueryParam, user_id: int, locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [
            markup.add(
                InlineKeyboardButton(
                    text=subject.name,
                    switch_inline_query_current_chat=f"{role} {query_param}_{subject.name}"))
            for subject
            in subjects
        ]

        classroom = InlineKeyboardButton(text=t(user_id, "ToClassroomIKBtn", locale), callback_data=f"{CallBackPrefix.ToClassroom} {locale}")
        markup.add(classroom)

        return markup

    @staticmethod
    def add_course_markup(courses: List[SubjectDto], locale: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name,
                                 callback_data=f"{CallBackPrefix.AddCourse} {course.id} {course.name} {locale}"))
            for course
            in courses]

        return markup

    @staticmethod
    def sub_course_markup(courses: List[SubjectDto]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        [markup.add(
            InlineKeyboardButton(text=course.name, switch_inline_query_current_chat=f"Subscribe_{course.name}"))
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
    def private_course_markup(
            private_course_id: int,
            role: Literal[Role.Tutor, Role.Student],
            locale,
            user_id: int,
            hide_all_classes_btn=False
    ) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()

        if web_app_link is not None:
            # TODO - think about adding role to an url
            plan_class_btn = InlineKeyboardButton(text=t(user_id, "PlanClassIKBtn", locale),
                                                  web_app=WebAppInfo(url=f"{web_app_link}/private-course/{private_course_id}"))
            markup.add(plan_class_btn)

        if not hide_all_classes_btn:
            all_classes_btn = InlineKeyboardButton(text=t(user_id, "AllClassesIKBtn", locale),
                                                   callback_data=f"{CallBackPrefix.CourseClasses} {private_course_id} {role} {locale}")
            markup.add(all_classes_btn)

        back_btn = InlineKeyboardButton(text=t(user_id, "BackIKBtn", locale),
                                        callback_data=f"{CallBackPrefix.BackToChoosePrivateCourse} {role} {locale}")

        markup.add(back_btn)

        return markup


class CustomInlineKeyboardMarkup(InlineKeyboardMarkup):
    def add_row(self, buttons: List[InlineKeyboardButton], row_width=None):
        if row_width is None:
            row_width = self.row_width

        for row in service_utils.chunks(buttons, row_width):
            button_array = [button for button in row]
            self.keyboard.append(button_array)

        return self

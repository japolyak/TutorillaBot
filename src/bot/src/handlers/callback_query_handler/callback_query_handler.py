from telebot.types import CallbackQuery
from telebot.states.sync.context import StateContext

from src.core.bot.bot import bot

from src.bot.src.handlers.callback_query_handler.actions.registration_actions import RegistrationActions
from src.bot.src.handlers.callback_query_handler.actions.student_actions import StudentActions
from src.core.bot.enums import CallBackPrefix


actions = {
    # Registration actions
    CallBackPrefix.SetUserLocale: RegistrationActions.registration_locale,
    CallBackPrefix.SetTimeZone: RegistrationActions.registration_time_zone,
    CallBackPrefix.BecomeTutor: RegistrationActions.select_role,
    CallBackPrefix.BecomeStudent: RegistrationActions.select_role,

    # Shared actions
    # CallBackPrefix.CourseClasses: SharedActions.get_course_classes,
    # CallBackPrefix.LoadPage: SharedActions.load_page,
    #
    # Tutor actions
    # CallBackPrefix.AddCourse: TutorActions.add_course_callback,
    # CallBackPrefix.BackToPrivateCourse: TutorActions.back_to_private_course,
    # CallBackPrefix.BackToChoosePrivateCourse: TutorActions.back_to_choose_subject_callback,
    # CallBackPrefix.GetTutorCoursesForPanel: TutorActions.tutor_course_panel,
    # CallBackPrefix.BackToOffice: TutorActions.back_to_office,
    # CallBackPrefix.BackToCourses: TutorActions.back_to_courses,
    # CallBackPrefix.BackToCourse: TutorActions.tutor_course_panel,
    # CallBackPrefix.CourseTextbooks: TutorActions.load_course_textbooks,
    # CallBackPrefix.AddTextbooks: TutorActions.add_textbooks,
    # CallBackPrefix.SaveTextbooks: TutorActions.save_textbooks,

    # Student actions
    CallBackPrefix.SubscribeCourse: StudentActions.subscribe_course,
    CallBackPrefix.ReturnToSelect: StudentActions.return_to_select,
    CallBackPrefix.FindTutor: StudentActions.find_tutor,
    CallBackPrefix.ToClassroom: StudentActions.to_classroom,
}


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery, redis, state: StateContext, *args, **kwargs):
    action_prefix, *arguments = call.data.split()

    fn_to_call = actions.get(action_prefix)

    if not fn_to_call:
        return

    fn_to_call(call, arguments, redis=redis, state=state)

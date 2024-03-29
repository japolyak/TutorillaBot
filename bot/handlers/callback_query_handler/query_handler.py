from bot.bot_token import bot
from telebot.types import CallbackQuery
from bot.handlers.callback_query_handler.callback_prefix import CallBackPrefix
from bot.handlers.callback_query_handler.actions.shared_actions import SharedActions
from bot.handlers.callback_query_handler.actions.student_actions import StudentActions
from bot.handlers.callback_query_handler.actions.tutor_actions import TutorActions
from bot.handlers.callback_query_handler.actions.admin_actions import AdminActions
from bot.handlers.callback_query_handler.actions.registration_actions import RegistrationActions


actions = {
    CallBackPrefix.AddCourse: TutorActions.add_course_callback,
    CallBackPrefix.BackToPrivateCourse: TutorActions.back_to_private_course,
    CallBackPrefix.BackToChoosePrivateCourse: TutorActions.back_to_choose_subject_callback,
    CallBackPrefix.RoleRequest: AdminActions.open_user_request,
    CallBackPrefix.AcceptRole: AdminActions.accept_user_request,
    CallBackPrefix.DeclineRole: AdminActions.decline_user_request,
    CallBackPrefix.BackToUsersRequests: AdminActions.back_to_requests,
    CallBackPrefix.SetUserLocale: RegistrationActions.registration_locale,
    CallBackPrefix.SetTimeZone: RegistrationActions.registration_time_zone,
    CallBackPrefix.CourseClasses: SharedActions.get_course_classes,
    CallBackPrefix.LoadPage: SharedActions.load_page,
    CallBackPrefix.SubscribeCourse: StudentActions.subscribe_course_callback,
    CallBackPrefix.ReturnToSelect: StudentActions.return_to_select_callback,
    CallBackPrefix.BecomeTutor: RegistrationActions.select_role,
    CallBackPrefix.BecomeStudent: RegistrationActions.select_role
}


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery):
    callback_data = call.data.split()

    action = CallBackPrefix(callback_data[0])

    if action not in actions.keys():
        return

    fn_to_call = actions.get(action)

    fn_to_call(call, callback_data[1:])

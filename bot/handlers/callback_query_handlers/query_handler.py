from bot.bot_token import bot
from telebot.types import CallbackQuery
from bot.handlers.callback_query_handlers.callback_prefix import CallBackPrefix
from bot.handlers.callback_query_handlers.actions.shared import get_course_classes, load_page
from bot.handlers.callback_query_handlers.actions.student import subscribe_course_callback, return_to_select_callback
from bot.handlers.callback_query_handlers.actions.tutor import back_to_private_course, back_to_choose_subject_callback, add_course_callback
from bot.handlers.callback_query_handlers.actions.admin import open_user_request, accept_user_request, decline_user_request, back_to_requests
from bot.handlers.callback_query_handlers.actions.registration import registration_locale, registration_time_zone, select_role


actions = {
    CallBackPrefix.AddCourse: add_course_callback,
    CallBackPrefix.BackToPrivateCourse: back_to_private_course,
    CallBackPrefix.BackToChoosePrivateCourse: back_to_choose_subject_callback,
    CallBackPrefix.RoleRequest: open_user_request,
    CallBackPrefix.AcceptRole: accept_user_request,
    CallBackPrefix.DeclineRole: decline_user_request,
    CallBackPrefix.BackToUsersRequests: back_to_requests,
    CallBackPrefix.SetUserLocale: registration_locale,
    CallBackPrefix.SetTimeZone: registration_time_zone,
    CallBackPrefix.CourseClasses: get_course_classes,
    CallBackPrefix.LoadPage: load_page,
    CallBackPrefix.SubscribeCourse: subscribe_course_callback,
    CallBackPrefix.ReturnToSelect: return_to_select_callback,
    CallBackPrefix.BecomeTutor: select_role,
    CallBackPrefix.BecomeStudent: select_role
}


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call: CallbackQuery):
    callback_data = call.data.split()

    action = CallBackPrefix(callback_data[0])

    if action not in actions.keys():
        return

    fn_to_call = actions.get(action)

    fn_to_call(call, callback_data[1:])

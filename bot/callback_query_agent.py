from telebot.types import CallbackQuery
from bot.enums import CallBackPrefix
from typing import Any, List


def get_callback_query_data(prefix: CallBackPrefix, call: CallbackQuery) -> List[Any]:
    cb_data = call.data.split()[1:]

    match prefix:
        case CallBackPrefix.BackToChoosePrivateCourse:
            return [cb_data[0]]

        case CallBackPrefix.BackToUsersRequests:
            return [cb_data[0]]

        case CallBackPrefix.RoleRequest:
            return [int(cb_data[0])]

        case CallBackPrefix.SubscribeCourse:
            return [int(cb_data[0])]

        case CallBackPrefix.AddCourse:
            return [int(cb_data[0])]

        case CallBackPrefix.DeclineRole:
            return [int(cb_data[0])]

        case CallBackPrefix.BackToPrivateCourse:
            return [int(cb_data[0]), cb_data[1]]

        case CallBackPrefix.AcceptRole:
            return [int(cb_data[0]), cb_data[1]]

        case CallBackPrefix.CourseClasses:
            return [int(cb_data[0]), cb_data[1]]

        case CallBackPrefix.LoadPage:
            return [int(cb_data[0]), int(cb_data[1]), cb_data[2], cb_data[3]]

        case _:
            return []

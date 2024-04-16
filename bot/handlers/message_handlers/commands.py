from bot.handlers.message_handlers.contexts.main_view import MainView
from bot.handlers.message_handlers.contexts.tutor import Tutor
from bot.handlers.message_handlers.contexts.student import Student
from bot.handlers.message_handlers.contexts.admin import Admin


translations = {
    "en-US": {
        "Main menu": "main_menu",
        "Office": "my_office",
        "My courses": "tutor_courses",
        "Add course": "add_course",
        "Classroom": "open_classroom",
        "My classes": "student_courses",
        "Subscribe course": "subscribe_course",
        "Admin panel": "show_admin_panel",
        "Tutor requests": "get_tutor_role_requests",
        "Student requests": "get_student_role_requests",
    }
}

command_handlers = {
    "main_menu": MainView.main_menu,
    "my_office": Tutor.my_office,
    "tutor_courses": Tutor.tutor_courses,
    "add_course": Tutor.add_course,
    "open_classroom": Student.open_classroom,
    "student_courses": Student.student_courses,
    "subscribe_course": Student.subscribe_course,
    "show_admin_panel": Admin.show_admin_panel,
    "get_tutor_role_requests": Admin.get_tutor_role_requests,
    "get_student_role_requests": Admin.get_student_role_requests,
}

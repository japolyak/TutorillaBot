from bot.handlers.message_handlers.contexts.main_view_context import MainViewContext
from bot.handlers.message_handlers.contexts.tutor_context import TutorContext
from bot.handlers.message_handlers.contexts.student_context import StudentContext
from bot.handlers.message_handlers.contexts.admin_context import AdminContext


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
    "main_menu": MainViewContext.main_menu,
    "my_office": TutorContext.my_office,
    "tutor_courses": TutorContext.tutor_courses,
    "add_course": TutorContext.add_course,
    "open_classroom": StudentContext.open_classroom,
    "student_courses": StudentContext.student_courses,
    "subscribe_course": StudentContext.subscribe_course,
    "show_admin_panel": AdminContext.show_admin_panel,
    "get_tutor_role_requests": AdminContext.get_tutor_role_requests,
    "get_student_role_requests": AdminContext.get_student_role_requests,
}

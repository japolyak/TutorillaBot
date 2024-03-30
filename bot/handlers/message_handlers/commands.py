from bot.handlers.message_handlers.contexts.mainview import MainView
from bot.handlers.message_handlers.contexts.tutor import Tutor
from bot.handlers.message_handlers.contexts.student import Student
from bot.handlers.message_handlers.contexts.admin import Admin


command_handlers = {
    MainView.main_menu.__name__: MainView.main_menu,
    Tutor.my_office.__name__: Tutor.my_office,
    Tutor.tutor_courses.__name__: Tutor.tutor_courses,
    Tutor.add_course.__name__: Tutor.add_course,
    Student.open_classroom.__name__: Student.open_classroom,
    Student.student_courses.__name__: Student.student_courses,
    Student.subscribe_course.__name__: Student.subscribe_course,
    Admin.show_admin_panel.__name__: Admin.show_admin_panel,
    Admin.get_tutor_role_requests.__name__: Admin.get_tutor_role_requests,
    Admin.get_student_role_requests.__name__: Admin.get_student_role_requests,
}


translations = {
    "en-US": {
        "Main menu": MainView.main_menu.__name__,
        "Office": Tutor.my_office.__name__,
        "My courses": Tutor.tutor_courses.__name__,
        "Add course": Tutor.add_course.__name__,
        "Classroom": Student.open_classroom.__name__,
        "My classes": Student.student_courses.__name__,
        "Subscribe course": Student.subscribe_course.__name__,
        "Admin panel": Admin.show_admin_panel.__name__,
        "Tutor requests": Admin.get_tutor_role_requests.__name__,
        "Student requests": Admin.get_student_role_requests.__name__,
    }
}

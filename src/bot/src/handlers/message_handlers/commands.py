from src.bot.src.handlers.message_handlers.contexts.main_view_context import MainViewContext
from src.bot.src.handlers.message_handlers.contexts.student_context import StudentContext
from src.bot.src.handlers.message_handlers.contexts.tutor_context import TutorContext
from src.bot.src.handlers.message_handlers.registration import RegistrationContext
# from src.bot.src.handlers.message_handlers.contexts.textbook_context import TextbookContext
# from src.bot.src.states import TextbookState

translations = {
    "en-US": {
        "Main menu": "main_menu",
        # "Office": "my_office",
        "Courses": "tutor_courses",
        "Students": "tutor_students",
        "Add course": "add_course",
        # "Classroom": "open_classroom",
        "My classes": "student_courses",
        "Subscribe course": "subscribe_course",
    }
}

command_handlers = {
    # Slash commands
    "start": RegistrationContext.start_function,

    "main_menu": MainViewContext.main_menu,
    "my_office": TutorContext.my_office,
    "tutor_courses": TutorContext.tutor_courses,
    "tutor_students": TutorContext.tutor_students,
    "add_course": TutorContext.add_course,
    "open_classroom": StudentContext.open_classroom,
    "student_courses": StudentContext.student_courses,
    "subscribe_course": StudentContext.subscribe_course,
}

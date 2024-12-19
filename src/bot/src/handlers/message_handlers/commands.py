from src.bot.src.handlers.message_handlers.contexts.student_context import StudentContext
from src.bot.src.handlers.message_handlers.contexts.admin_context import AdminContext
from src.bot.src.handlers.message_handlers.contexts.user_context import UserContext
from src.bot.src.handlers.message_handlers.registration import RegistrationContext


translations = {
    "en-US": {
        "Support": "support",
        "Profile": "open_profile",
        "Classroom": "open_classroom",
        "Admin panel": "admin_panel",
    }
}

command_handlers = {
    # Slash commands
    "start": RegistrationContext.start_function,

    #Text commands
    "support": UserContext.support,
    "open_profile": UserContext.open_profile,
    "open_classroom": StudentContext.open_classroom,
    "admin_panel": AdminContext.admin_panel,
}

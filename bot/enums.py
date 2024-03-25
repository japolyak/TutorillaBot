from enum import Enum, StrEnum


class CallBackPrefix(StrEnum):
    """
    An Enum for callback prefixes

    : This Enum serves the purpose of encapsulating various prefixes used in callback data.

    In essence, each value is a concatenation of the first letters of each word in the key, separated by underscores.
    This convention is employed to ensure that the length of callback data does not exceed the 64-byte limit imposed by Telegram.
    """

    AddCourse = "a_c"
    AcceptRole = "a_r"
    BecomeTutor = "b_t"
    BackToAdminPanel = "b_t_a_p"
    BackToPrivateCourse = "b_t_p_c"
    BackToChoosePrivateCourse = "b_t_c_p_c"
    BackToUsersRequests = "b_t_u_r"
    BecomeStudent = "b_s"
    CourseClasses = "c_c"
    DeclineRole = "d_r"
    EmptyCallback = "e_c"
    InvoicesForTutor = "i_f_t"
    LoadPage = "l_p"
    PrivateClass = "p_c"
    RoleRequest = "r_r"
    ReturnToSelect = "r_t_s"
    SubscribeCourse = "s_c"
    SetEmail = "s_e"
    SetFirstName = "s_f_n"
    SetLastName = "s_l_n"
    SetPhone = "s_p"


class Emoji(Enum):
    ClassScheduled = u'\U0001F4C5'
    ClassOccurred = u'\U00002705'
    ClassPaid = u'\U0001F4B0'
    BackArrow = u'\u2B05'
    NextArrow = u'\u27A1'
    Accept = u'\u2714'
    Decline = u'\u274C'


class Role(StrEnum):
    Tutor = "tutor"
    Student = "student"
    Admin = "admin"

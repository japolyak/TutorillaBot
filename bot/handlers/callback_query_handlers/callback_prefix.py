from enum import StrEnum


class CallBackPrefix(StrEnum):
    """
    An Enum for callback prefixes

    This Enum serves the purpose of encapsulating various prefixes used in callback data.

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
    SetTimeZone = "s_t_z"
    SetUserLocale = "s_u_l"
from enum import StrEnum


class CallBackPrefix(StrEnum):
    """
    An Enum for callback prefixes

    This Enum serves the purpose of encapsulating various prefixes used in callback data.

    In essence, each value is a concatenation of the first letters of each word in the key, separated by underscores.
    This convention is employed to ensure that the length of callback data does not exceed the 64-byte limit imposed by Telegram.
    """

    AcceptRole = "a_r"
    AddCourse = "a_c"
    AddTextbooks = "a_t"
    BecomeTutor = "b_t"
    BackToAdminPanel = "b_t_a_p"
    BackToCourse = "b_t_c"
    BackToCourses = "b_t_cs"
    BackToOffice = "b_t_o"
    BackToPrivateCourse = "b_t_p_c"
    BackToChoosePrivateCourse = "b_t_c_p_c"
    BackToUsersRequests = "b_t_u_r"
    BecomeStudent = "b_s"
    CourseClasses = "c_c"
    CourseTextbooks = "c_t"
    DeclineRole = "d_r"
    EmptyCallback = "e_c"
    GetTutorCoursesForPanel = "g_t_c_f_p"
    InvoicesForTutor = "i_f_t"
    LoadPage = "l_p"
    PrivateClass = "p_c"
    RoleRequest = "r_r"
    ReturnToSelect = "r_t_s"
    SaveTextbooks = "s_t"
    SetEmail = "s_e"
    SetFirstName = "s_f_n"
    SetLastName = "s_l_n"
    SetTimeZone = "s_t_z"
    SetUserLocale = "s_u_l"
    ShowTextbook = "s_t"
    SubscribeCourse = "s_c"

class APIEndpoints:
    class TutorCourse:
        Prefix = "/tutor-courses"
        AddCourse = "/users/{user_id}/"
        GetCourses = "/users/{user_id}/"
        AvailableCourses = "/users/{user_id}/subject-name/{subject_name}/"

    class Users:
        Prefix = "/users"
        Post = "/"
        GetUser = "/{user_id}/"
        ApplyRole = "/{user_id}/apply-role/{role}/"

    class PrivateCourses:
        Prefix = "/private-courses"
        GetPrivateCourse = "/{private_course_id}/"
        GetClasses = "/{course_id}/classes/"
        GetClassesByDate = "/{private_course_id}/classes/month/{month}/year/{year}/"
        Get = "/users/{user_id}/subjects/{subject_name}/"
        Enroll = "/{private_course_id}/users/{user_id}/"
        AddNewClass = "/{private_course_id}/new-class/{role}/"

    class Admin:
        Prefix = "/admin"
        RequestsStatistics = "/requests-statistics/"
        GetRequest = "/user-requests/{role_request_id}/"
        GetRequests = "/role-requests/{role}/"
        AcceptRole = "/users/{user_id}/accept-role/{role}/"
        DeclineRole = "/users/{user_id}/decline-role/"

    class Subjects:
        Prefix = "/subjects"
        Get = "/users/{user_id}/available/{is_available}/"

    class WebApp:
        Prefix = "/auth"
        Me = "/me/"

    class Textbook:
        Prefix = "/textbooks"
        Get = "/tutor-course/{tutor_course_id}/"
        Post = "/tutor-course/{tutor_course_id}/"
        Delete = "/textbook_id/"

    class Home:
        Prefix = "/home"
        Get = "/"

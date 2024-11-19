class APIEndpoints:
    class TutorCourse:
        Prefix = "/tutor-courses"
        AddCourse = "/users/{user_id}/"
        GetCourses = "/users/{user_id}/"
        AvailableCourses = "/users/{user_id}/subject-name/{subject_name}/"

    class Users:
        Prefix = "/users"
        Post = "/"
        Me = "/me/"
        ApplyRole = "/apply-role/{role}/"

    class Events:
        Prefix = "/events"
        Range = "/start/{start}/end/{end}/"
        CreateClass = "/class/courses/{private_course_id}/"

    class PrivateCourses:
        Prefix = "/private-courses"
        Get = "/"
        GetPrivateCourse = "/{private_course_id}/"
        GetClasses = "/{course_id}/classes/"
        GetBySubjects = "/users/{user_id}/subjects/{subject_name}/"
        Enroll = "/{private_course_id}/users/{user_id}/"

    class Admin:
        Prefix = "/admin"
        RequestsStatistics = "/requests-statistics/"
        GetRequests = "/role-requests/{role}/"
        AcceptRole = "/role-requests/{request_id}/accept/"
        DeclineRole = "/role-requests/{request_id}/decline/"

    class Subjects:
        Prefix = "/subjects"
        Get = "/users/{user_id}/available/{is_available}/"

    class Authentication:
        Prefix = "/auth"
        Me = "/me/"
        Tg = "/tg/"

    class Textbook:
        Prefix = "/textbooks"
        Get = "/tutor-course/{tutor_course_id}/"
        Post = "/tutor-course/{tutor_course_id}/"
        Delete = "/textbook_id/"

    class Home:
        Prefix = "/home"
        Get = "/"

from itertools import groupby
from operator import attrgetter

from src.core.models import ScheduleCoursePersonDto, ScheduleCourseDto


class ModelUtils:
    @staticmethod
    def schedule_course_mapper(courses):
        grouped_courses = []

        for (subject_id, subject_name), items in groupby(courses, key=attrgetter('subject_id', 'subject_name')):
            grouped_items = [ScheduleCoursePersonDto.from_tuple(item[2:]) for item in items]

            if len(grouped_items) == 0:
                continue

            group = ScheduleCourseDto(subject_id=subject_id, subject_name=subject_name, persons=grouped_items)
            grouped_courses.append(group)

        return grouped_courses

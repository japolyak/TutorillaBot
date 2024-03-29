from enum import Enum, StrEnum


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

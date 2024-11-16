from sqlalchemy import String, BigInteger, Boolean, ForeignKey, UniqueConstraint, Integer, Float
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped, MappedColumn
from typing import List
from src.common.config import schema_name


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": schema_name}

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=False, primary_key=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="false")
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    normalized_email: Mapped[str] = mapped_column(String(255), unique=True)
    time_zone: Mapped[float] = mapped_column(Float)
    locale: Mapped[str] = mapped_column(String(10), server_default="en-US")
    is_tutor: Mapped[bool] = mapped_column(Boolean, server_default="false")
    is_student: Mapped[bool] = mapped_column(Boolean, server_default="false")
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default="false")

    tutor_courses: Mapped[List["TutorCourse"]] = relationship(
        "TutorCourse", back_populates="tutor", cascade="all, delete-orphan"
    )

    private_courses: Mapped[List["PrivateCourse"]] = relationship(
        "PrivateCourse", back_populates="student", cascade="all, delete-orphan"
    )

    user_request: Mapped["UserRequest"] = relationship("UserRequest", uselist=False, back_populates="user")


class UserRequest(Base):
    __tablename__ = "users_requests"
    __table_args__ = {"schema": schema_name}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(f"{schema_name}.users.id"))
    request_time_unix: Mapped[int] = mapped_column(BigInteger, server_default="0")
    role: Mapped[int] = mapped_column(Integer, server_default="0")

    user: Mapped["User"] = relationship("User", back_populates="user_request")


class Subject(Base):
    __tablename__ = "subjects"
    __table_args__ = {"schema": schema_name}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    tutor_courses: Mapped[List["TutorCourse"]] = relationship(
        "TutorCourse", back_populates="subject", cascade="all, delete-orphan"
    )


class TutorCourse(Base):
    __tablename__ = "tutor_courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey(f"{schema_name}.users.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey(f"{schema_name}.subjects.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true")
    price: Mapped[int] = mapped_column(Integer)

    tutor: Mapped["User"] = relationship("User", back_populates="tutor_courses")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="tutor_courses")

    __table_args__ = (
        UniqueConstraint(tutor_id, subject_id, name="unique_tutor_subject"),
        {"schema": schema_name}
    )

    private_courses: Mapped[List["PrivateCourse"]] = relationship(
        "PrivateCourse", back_populates="tutor_course", cascade="all, delete-orphan"
    )

    textbooks: Mapped[List["Textbook"]] = relationship(
        "Textbook", back_populates="tutor_course", cascade="all, delete-orphan"
    )


class PrivateCourse(Base):
    __tablename__ = "private_courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey(f"{schema_name}.users.id"))
    tutor_course_id: Mapped[int] = mapped_column(ForeignKey(f"{schema_name}.tutor_courses.id"))
    price: Mapped[int] = mapped_column(Integer)

    student: Mapped["User"] = relationship("User", back_populates="private_courses")
    tutor_course: Mapped["TutorCourse"] = relationship("TutorCourse", back_populates="private_courses")

    __table_args__ = (
        UniqueConstraint(student_id, tutor_course_id, name="unique_student_course"),
        {"schema": schema_name}
    )

    private_classes: Mapped[List["PrivateClass"]] = relationship(
        "PrivateClass", back_populates="private_course", cascade="all, delete-orphan"
    )


class PrivateClass(Base):
    __tablename__ = "private_classes"
    __table_args__ = {"schema": schema_name}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    private_course_id: Mapped[int] = mapped_column(ForeignKey(f"{schema_name}.private_courses.id"))
    start_time_unix: Mapped[int] = mapped_column(BigInteger, server_default="0")
    duration: Mapped[int] = mapped_column(Integer, server_default="0")
    is_scheduled: Mapped[bool] = mapped_column(Boolean, server_default="true")
    has_occurred: Mapped[bool] = mapped_column(Boolean, server_default="false")
    is_paid: Mapped[bool] = mapped_column(Boolean, server_default="false")

    private_course: Mapped["PrivateCourse"] = relationship("PrivateCourse", back_populates="private_classes")


class Textbook(Base):
    __tablename__ = "textbooks"

    id: MappedColumn[int] = mapped_column(primary_key=True, index=True)
    title: MappedColumn[str] = mapped_column(String(255))
    tutor_course_id: MappedColumn[int] = mapped_column(ForeignKey(f"{schema_name}.tutor_courses.id"))

    tutor_course: Mapped["TutorCourse"] = relationship("TutorCourse", back_populates="textbooks")

    __table_args__ = (
        UniqueConstraint(title, tutor_course_id, name="unique_textbook_tutor_course"),
        {"schema": schema_name}
    )

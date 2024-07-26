import datetime
from pydantic import BaseModel
from typing import Optional

class IdSchema(BaseModel):
    id: int

class SchoolGrade(BaseModel):
    grade: str
    price: float

class User(BaseModel):
    id: int
    name: str
    surname: str
    username: str
    birthdate: datetime.date

class Student(BaseModel):
    id: int
    user: User

class Teacher(BaseModel):
    id: int

class Subject(BaseModel):
    name: str

class BookingSchema(BaseModel):
    teacher: Optional[Teacher]
    student: Optional[Student]
    subject: Subject
    school_grade: SchoolGrade
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    duration: int
    notes: str
    attended: bool
    insert_id_user: int
    insert_date: datetime.date
    insert_time: datetime.time

class CreateBookingSchema(BaseModel):
    email_teacher: str
    email_student: str
    id_subject: int
    id_school_grade: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    notes: Optional[str]
    attended: bool
    insert_id_user: int
    insert_date: datetime.date
    insert_time: datetime.time

class FullCalendarBookingSchema(BaseModel):
    id_booking: int
    title: str
    start: datetime.datetime
    end: datetime.datetime
    allDay: bool

class StudentInfoResponse(BaseModel):
    user: User
    school_grade: Optional[SchoolGrade]


class TeacherInfoResponse(BaseModel):
    user: User
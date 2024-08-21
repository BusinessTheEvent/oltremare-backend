import datetime
from pydantic import BaseModel
from typing import Optional

class IdSchema(BaseModel):
    id: int

class SchoolGrade(BaseModel):
    id_school_grade: int
    grade: str
    price: float

class User(BaseModel):
    id: int
    name: str
    surname: Optional[str]
    username: str
    birthdate: Optional[datetime.date]

class UpdateUserSchema(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    username: Optional[str]
    password: Optional[str]

class UpdateStudentSchema(BaseModel):
    id_school_grade: Optional[int]
    name: Optional[str]
    surname: Optional[str]
    password: Optional[str]
    username: Optional[str]

class TeacherSchoolSubjectSchema(BaseModel):
    id: int
    id_school_grade: int
    id_subject: int

class SchoolLevelSchema(BaseModel):
    level: str
    isChecked: bool

class SubjectPatchSchema(BaseModel):
    id: int
    name: Optional[str]
    isChecked: bool
    levels: Optional[list[SchoolLevelSchema]]

class UpdateTeacherSchema(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    username: Optional[str]
    password: Optional[str]
    teacher_subjects: Optional[list[SubjectPatchSchema]]

class Student(BaseModel):
    id: int
    user: User

class Teacher(BaseModel):
    id: int
    user: User

class SubjectSchema(BaseModel):
    id_subject: int
    name: str
    

class BookingSchema(BaseModel):
    teacher: Optional[Teacher]
    student: Optional[Student]
    subject: SubjectSchema
    school_grade: SchoolGrade
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    duration: int
    notes: str
    attended: bool
    insert_id_user: int
    insert_date: datetime.date
    insert_time: datetime.time
    price: Optional[float] = 0.0

class CreateBookingSchema(BaseModel):
    id_teacher: int
    id_student: int
    id_subject: int
    duration: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    notes: Optional[str] = ""
    insert_id_user: int

class FullCalendarBookingSchema(BaseModel):
    id_booking: int
    title: str
    start: datetime.datetime
    end: datetime.datetime
    allDay: bool

class StudentInfoResponse(BaseModel):
    user: User
    school_grade: Optional[SchoolGrade]
    preliminary_meeting: Optional[bool]


class TeacherInfoResponse(BaseModel):
    user: User
    subjects: list[SubjectSchema]

class MessageResponse(BaseModel):
    id_message: int
    sender: User
    receiver: User
    text: str
    send_datetime: datetime.datetime

class CreateUserSchema(BaseModel):
    surname: str
    email: str
    name: str
    password: str
    school: str
    type: str

class PreliminaryMeetingSchema(BaseModel):
    done: bool
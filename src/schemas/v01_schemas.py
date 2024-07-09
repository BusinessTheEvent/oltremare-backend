import datetime
from pydantic import BaseModel

class SchoolGrade(BaseModel):
    id_school_grade: int
    grade: str
    price: float

class Student(BaseModel):
    id: int
    id_school_grade: int
    preliminary_meeting: bool

class Teacher(BaseModel):
    id: int

class Subject(BaseModel):
    id_subject: int
    name: str

class Booking(BaseModel):
    id_booking: int
    id_student: int
    id_teacher: int
    id_school_grade: int
    id_subject: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    duration: int
    notes: str
    insert_id_user: int
    insert_date: datetime.date
    insert_time: datetime.time

class TeacherSchoolSubject(BaseModel):
    id: int
    id_school_grade: int
    id_subject: int

class Chief(BaseModel):
    id: int

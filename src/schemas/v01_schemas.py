import datetime
from pydantic import BaseModel
import datetime
from pydantic import BaseModel

class SchoolGrade(BaseModel):
    grade: str
    price: float

class Student(BaseModel):
    id: int
    name: str
    surname: str
    username: str

class Teacher(BaseModel):
    id: int

class Subject(BaseModel):
    name: str

class BookingSchema(BaseModel):
    teacher: Teacher
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

class BookingResponseSchema(BaseModel):
    student_data: Student
    booking_data: BookingSchema

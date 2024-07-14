import datetime
from pydantic import BaseModel
from typing import Optional

class SchoolGrade(BaseModel):
    grade: str
    price: float

class User(BaseModel):
    id: int
    name: str
    surname: str
    username: str

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
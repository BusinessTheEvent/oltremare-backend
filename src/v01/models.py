from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, DateTime, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.auth.models import User
from src.databases.db import Base
from dailyscheduler.abstract_classes import Task

class SchoolGrade(Base):
    __tablename__ = 'school_grade'
    id_school_grade = Column(Integer, primary_key=True)
    grade = Column(String, nullable=False)
    price = Column(Numeric(8, 2), nullable=False)

    bookings = relationship('Booking', back_populates='school_grade')

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    id_school_grade = Column(Integer, ForeignKey('school_grade.id_school_grade'), nullable=False)
    preliminary_meeting = Column(Boolean, nullable=False)

    bookings = relationship('Booking')
    user = relationship('User')

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    user = relationship('User')
    bookings = relationship('Booking', back_populates='teacher')
    subjects = relationship('Subject', secondary='teacher_school_subject')

class Subject(Base):
    __tablename__ = 'subjects'
    id_subject = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    bookings = relationship('Booking', back_populates='subject')

class Booking(Base):
    __tablename__ = 'booking'
    id_booking = Column(Integer, primary_key=True)
    id_student = Column(Integer, ForeignKey('student.id'), nullable=False)
    id_teacher = Column(Integer, ForeignKey('teacher.id'), nullable=False)
    id_school_grade = Column(Integer, ForeignKey('school_grade.id_school_grade'), nullable=False)
    id_subject = Column(Integer, ForeignKey('subjects.id_subject'), nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    notes = Column(String)
    attended = Column(Boolean, nullable=False)
    insert_id_user = Column(Integer, nullable=False)
    insert_date = Column(Date, nullable=False)
    insert_time = Column(Time, nullable=False)

    student = relationship('Student', back_populates='bookings')
    school_grade = relationship('SchoolGrade', back_populates='bookings')
    teacher = relationship('Teacher', back_populates='bookings')
    subject = relationship('Subject', back_populates='bookings')



class TeacherSchoolSubject(Base):
    __tablename__ = 'teacher_school_subject'
    id = Column(Integer, ForeignKey('teacher.id'), primary_key=True)
    id_school_grade = Column(Integer, ForeignKey('school_grade.id_school_grade'), primary_key=True)
    id_subject = Column(Integer, ForeignKey('subjects.id_subject'), primary_key=True)

class Chief(Base):
    __tablename__ = 'chief'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class BookingTask(Task):
    id_booking: int
    id_student: int
    id_teacher: int
    id_school_grade: int
    id_subject: int
    start_datetime: DateTime
    end_datetime: DateTime
    duration: int
    notes: str
    attended: bool
    insert_id_user: int
    insert_date: Date
    insert_time: Time

    def __init__(self, booking: Booking):
        super().__init__(id=booking.id_booking, from_hour=booking.start_datetime.time(), to_hour=booking.end_datetime.time())

        self.id_booking = booking.id_booking
        self.id_student = booking.id_student
        self.id_teacher = booking.id_teacher
        self.id_school_grade = booking.id_school_grade
        self.id_subject = booking.id_subject
        self.start_datetime = booking.start_datetime
        self.end_datetime = booking.end_datetime
        self.duration = booking.duration
        self.notes = booking.notes
        self.attended = booking.attended
        self.insert_id_user = booking.insert_id_user
        self.insert_date = booking.insert_date
        self.insert_time = booking.insert_time

    def __str__(self):
        return f'{self.id_booking} - {self.start_datetime} - {self.end_datetime} - {self.duration} - {self.notes} - {self.attended} - {self.insert_id_user} - {self.insert_date} - {self.insert_time}'

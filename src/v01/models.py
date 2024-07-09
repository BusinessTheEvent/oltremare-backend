from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, DateTime, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.auth.models import User
Base = declarative_base()

class SchoolGrade(Base):
    __tablename__ = 'school_grade'
    id_school_grade = Column(Integer, primary_key=True)
    grade = Column(String, nullable=False)
    price = Column(Numeric(8, 2), nullable=False)

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    id_school_grade = Column(Integer, ForeignKey('school_grade.id_school_grade'), nullable=False)
    preliminary_meeting = Column(Boolean, nullable=False)

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)

class Subject(Base):
    __tablename__ = 'subjects'
    id_subject = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

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
    insert_id_user = Column(Integer, nullable=False)
    insert_date = Column(Date, nullable=False)
    insert_time = Column(Time, nullable=False)
    
    def _init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class TeacherSchoolSubject(Base):
    __tablename__ = 'teacher_school_subject'
    id = Column(Integer, ForeignKey('teacher.id'), primary_key=True)
    id_school_grade = Column(Integer, ForeignKey('school_grade.id_school_grade'), primary_key=True)
    id_subject = Column(Integer, ForeignKey('subjects.id_subject'), primary_key=True)

class Chief(Base):
    __tablename__ = 'chief'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    

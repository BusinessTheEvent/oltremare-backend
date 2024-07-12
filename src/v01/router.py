from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.auth.models import User
from src.v01.models import Booking, Teacher, Student, TeacherSchoolSubject, Subject, SchoolGrade
from src.databases.db import get_db
from src.default_logger import get_custom_logger
from src.schemas.v01_schemas import BookingSchema
from fastapi import HTTPException
from sqlalchemy import extract  


logger = get_custom_logger(__name__)


router = APIRouter()
logger = get_custom_logger(__name__)

@router.get("/")
def healtcheck():
    return {"status": "ok", "version": "0.1"}

#accessibile solo da admin
@router.get("/users/all")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

#accessibile solo da admin e insegnante (per gli studenti)
@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user
    
#accessibile solo da admin
@router.get("/booking/all")
def get_all_booking(db: Session = Depends(get_db)):
    booking = db.query(Booking).all()
    return booking

#get all teacher
@router.get("/booking/all_teacher")
def get_all_booking(db: Session = Depends(get_db)):
    # Query and join to get necessary data
    teachers_bookings = db.query(Teacher, Booking).join(Booking, Teacher.id == Booking.id_teacher).all()

    # Prepare the response in a serializable format
    result = []
    for teacher, booking in teachers_bookings:
        teacher_data = {
            'id': teacher.id,
            # Include other attributes of Teacher model if needed
        }
        booking_data = {
            'id_booking': booking.id_booking,
            'id_student': booking.id_student,
            'id_teacher': booking.id_teacher,
            'id_school_grade': booking.id_school_grade,
            'id_subject': booking.id_subject,
            'start_datetime': booking.start_datetime,
            'end_datetime': booking.end_datetime,
            'duration': booking.duration,
            'notes': booking.notes,
            'attended': booking.attended,
            'insert_id_user': booking.insert_id_user,
            'insert_date': booking.insert_date,
            'insert_time': booking.insert_time
        }
        result.append({
            'teacher': teacher_data,
            'booking': booking_data
        })

    return result

#get teacher group by subject
@router.get("/booking/get_teacher_by_school_and_subject/{id_subject}{id_school_grade}")
def get_all_booking(id_subject: int, id_school_grade: int,db: Session = Depends(get_db)):
    # Query and join to get necessary data
    list = db.query(Teacher, TeacherSchoolSubject, Subject)\
                .join(Teacher, Teacher.id == TeacherSchoolSubject.id)\
                .join(Subject, Subject.id_subject == TeacherSchoolSubject.id_subject)\
                .filter(Subject.id_subject == id_subject, TeacherSchoolSubject.id_school_grade == id_school_grade)\
                .all()
    
    #TODO: finish and test this

    print(list)

    # Prepare the response in a serializable format
    result = []
    for teacher, teacherSchoolSubject, subject in list:
        teacher_data = {
            'id': teacher.id,
            # Include other attributes of Teacher model if needed
        }
        teacherSchoolSubject={
            'id': teacherSchoolSubject.id,
            'id_school_grade': teacherSchoolSubject.id_school_grade,
            'id_subject': teacherSchoolSubject.id_subject
        }
        subject={
            'id_subject': subject.id_subject,
            'name': subject.name
        }
        result.append({
            'teacher': teacher_data,
            'teacherSchoolSubject': teacherSchoolSubject,
            'subject': subject
        })

    return result
# SELECT teacher.id AS teacher_id, teacher_school_subject.id AS teacher_school_subject_id, teacher_school_subject.id_school_grade AS teacher_school_subject_id_school_grade, teacher_school_subject.id_subject AS teacher_school_subject_id_subject, subjects.id_subject AS subjeccts_id_subject, subjects.name AS subjects_name
# FROM teacher_school_subject JOIN teacher ON teacher.id = teacher_school_subject.id JOIN teacher_school_subject ON subjects.id_subject = teacher_school_subject.id_subject, subjects
# WHERE subjects.id_subject = 1 AND teacher_school_subject.id_school_grade = 1

#get all teacher group by subject
# @router.get("/booking/all_teacher_by_subject")
# def get_all_booking(db: Session = Depends(get_db)):
#     # Query and join to get necessary data
#     teacher_by_subject = db.query(User,Teacher).join(Teacher, User.id == Teacher.id).all()

#     # Prepare the response in a serializable format
#     result = []
#     for student, booking in teacher_by_subject:
#         students_data = {
#             'id': student.id,
#             # Include other attributes of Teacher model if needed
#         }
#         booking_data = {
#             'id_booking': booking.id_booking,
#             'id_student': booking.id_student,
#             'id_teacher': booking.id_teacher,
#             'id_school_grade': booking.id_school_grade,
#             'id_subject': booking.id_subject,
#             'start_datetime': booking.start_datetime,
#             'end_datetime': booking.end_datetime,
#             'duration': booking.duration,
#             'notes': booking.notes,
#             'attended': booking.attended,
#             'insert_id_user': booking.insert_id_user,
#             'insert_date': booking.insert_date,
#             'insert_time': booking.insert_time
#         }
#         result.append({
#             'student': students_data,
#             'booking': booking_data
#         })

#     return result

#get all student
@router.get("/booking/all_student")
def get_all_booking(db: Session = Depends(get_db)):
    # Query and join to get necessary data
    students_bookings = db.query(Student, Booking).join(Booking, Student.id == Booking.id_student).all()

    # Prepare the response in a serializable format
    result = []
    for student, booking in students_bookings:
        students_data = {
            'id': student.id,
            # Include other attributes of Teacher model if needed
        }
        booking_data = {
            'id_booking': booking.id_booking,
            'id_student': booking.id_student,
            'id_teacher': booking.id_teacher,
            'id_school_grade': booking.id_school_grade,
            'id_subject': booking.id_subject,
            'start_datetime': booking.start_datetime,
            'end_datetime': booking.end_datetime,
            'duration': booking.duration,
            'notes': booking.notes,
            'attended': booking.attended,
            'insert_id_user': booking.insert_id_user,
            'insert_date': booking.insert_date,
            'insert_time': booking.insert_time
        }
        result.append({
            'student': students_data,
            'booking': booking_data
        })

    return result


#accessibile da tutti
@router.get("/booking/{id_booking}")
def get_booking(id_booking: int, db: Session = Depends(get_db)):
    book = db.query(Booking).filter(Booking.id_booking == id_booking).first()
    return book

#tutte le prenotazioi di uno studente
@router.get("/booking/student/{id_student}")
def get_student_booking(id_student: int, db: Session = Depends(get_db)):
    book = db.query(Booking).filter(Booking.id_student == id_student).all()
    return book

#prenotazioni di un insegnante
@router.get("/booking/teacher/{id_teacher}")
def get_teacher_booking(id_teacher: int, db: Session = Depends(get_db)):
    book = db.query(Booking).filter(Booking.id_teacher == id_teacher).first()
    return book

#accessibile solo da admin e studente
#inserimento di una prenotazione
@router.put("/booking/insert")
def create_booking(booking_new: BookingSchema, db: Session = Depends(get_db)):    
    new_booking = Booking(**booking_new.model_dump())
    db.add(new_booking)
    db.commit()
    return HTTPException(status_code=200, detail="Ticket type created successfully")


#accessibile solo da admin e insegnante
#rimozione di una prenotazione
@router.delete("/booking/{id_booking}")
def delete_booking(id_booking: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id_booking == id_booking).first()
    db.delete(booking)
    db.commit()
    return HTTPException(status_code=200, detail="Booking deleted successfully")


#tutte le materie
@router.get("/subject/all_subject")
def get_all_subject(db: Session = Depends(get_db)):
    subject = db.query(Subject).all()
    return subject

#tutte le scuole
@router.get("/school/all_school_grade")
def get_all_school_grade(db: Session = Depends(get_db)):
    school = db.query(SchoolGrade).all()
    return school


#get booking by month per student
@router.get("/booking/get_booking_by_month_per_student/{month}{id_student}")
def get_booking_by_month_per_student(month: int, id_student: int, db: Session = Depends(get_db)):
    # Query and join to get necessary data
    booking = db.query(Booking).filter(extract('month', Booking.start_datetime) == month, Booking.id_student == id_student).all()
    return booking

#get booking by month per teacher
@router.get("/booking/get_booking_by_month_per_teacher/{month}{id_teacher}")
def get_booking_by_month_per_teacher(month: int, id_teacher: int, db: Session = Depends(get_db)):
    # Query and join to get necessary data
    booking = db.query(Booking).filter(extract('month', Booking.start_datetime) == month, Booking.id_teacher == id_teacher).all()
    return booking

#TODO: valutare se fare una query per ottenere il prezzo finale delle prentoazione mensili di un insegnante/studnete 
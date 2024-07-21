from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.auth.models import User
from src.v01.models import Booking, Teacher, TeacherSchoolSubject, Subject, SchoolGrade, AnagSlot
from src.databases.db import get_db
from src.default_logger import get_custom_logger
from src.schemas.v01_schemas import CreateBookingSchema, BookingSchema
from fastapi import HTTPException
from sqlalchemy import extract
from src.config import settings
import datetime
from dailyscheduler.classes import WorkingDay

START_HOUR = 9
END_HOUR = 18
SLOT_DURATION = 30
SLOTS_IN_HOUR = 60 // SLOT_DURATION

router = APIRouter()
logger = get_custom_logger(__name__)

@router.get("/")
def healtcheck():
    return {"status": "ok", "version": settings.APP_VERSION}

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

#get teacher group by subject
@router.get("/booking/get_teacher_by_school_and_subject/{id_school_grade}/{id_subject}")
def get_teacher_by_subject(id_subject: int, id_school_grade: int,db: Session = Depends(get_db)):
    # Query and join to get necessary data
    list = db.query(Teacher, TeacherSchoolSubject, Subject)\
                .join(Teacher, Teacher.id == TeacherSchoolSubject.id)\
                .join(Subject, Subject.id_subject == TeacherSchoolSubject.id_subject)\
                .filter(Subject.id_subject == id_subject, TeacherSchoolSubject.id_school_grade == id_school_grade)\
                .all()

    #TODO: finish and test this

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

# get all students' booking
@router.get("/booking/all_student", response_model=list[BookingSchema])
def get_all_students_booking(db: Session = Depends(get_db)) -> list[BookingSchema]:
    # Query and join to get necessary data
    students_bookings = db.query(Booking).all()

    return students_bookings

#accessibile da tutti
@router.get("/booking/{id_booking}", response_model=BookingSchema)
def get_booking(id_booking: int, db: Session = Depends(get_db)) -> BookingSchema:
    book = db.query(Booking).filter(Booking.id_booking == id_booking).first()
    return book

#tutte le prenotazioi di uno studente
@router.get("/booking/student/{id_student}", response_model=list[BookingSchema])
def get_student_booking(id_student: int, db: Session = Depends(get_db)) -> list[BookingSchema]:
    books = db.query(Booking).filter(Booking.id_student == id_student).all()
    return books

#prenotazioni di un insegnante
@router.get("/booking/teacher/{id_teacher}", response_model=list[BookingSchema])
def get_teacher_booking(id_teacher: int, db: Session = Depends(get_db)) -> list[BookingSchema]:
    bookings = db.query(Booking).filter(Booking.id_teacher == id_teacher).all()
    return bookings

#accessibile solo da admin e studente
#inserimento di una prenotazione
@router.put("/booking/insert")
def create_booking(booking_new: CreateBookingSchema, db: Session = Depends(get_db)):    
    ## TODO: add secutiry checks
    ## TODO: make utility function to execute complex query safely
    
    slots = db.query(AnagSlot).all()

    duration = (booking_new.end_datetime - booking_new.start_datetime).min

    new_booking = Booking(**booking_new.model_dump(), duration=duration)

    start_index = ((new_booking.start_datetime.hour - START_HOUR) * SLOTS_IN_HOUR + new_booking.start_datetime.minute // SLOT_DURATION) + 1
    end_index = ((new_booking.end_datetime.hour - START_HOUR) * SLOTS_IN_HOUR + new_booking.end_datetime.minute // SLOT_DURATION) + 1

    for slot in slots:
        if slot.id_slot >= start_index and slot.id_slot <= end_index:
            new_booking.slots.append(slot)
    
    db.add(new_booking)
    db.commit()
    return HTTPException(status_code=200, detail="Booking created successfully")

#accessibile solo da admin e insegnante
#rimozione di una prenotazione
@router.delete("/booking/{id_booking}")
def delete_booking(id_booking: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id_booking == id_booking).first()
    db.delete(booking)



    ## TODO: implement on cascade?
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
@router.get("/booking/get_booking_by_month_per_student/{month}/{id_student}")
def get_booking_by_month_per_student(month: int, id_student: int, db: Session = Depends(get_db)):
    # Query and join to get necessary data
    booking = db.query(Booking).filter(extract('month', Booking.start_datetime) == month, Booking.id_student == id_student).all()
    return booking

#get booking by month per teacher
@router.get("/booking/get_booking_by_month_per_teacher/{month}/{id_teacher}")
def get_booking_by_month_per_teacher(month: int, id_teacher: int, db: Session = Depends(get_db)):
    # Query and join to get necessary data
    booking = db.query(Booking).filter(extract('month', Booking.start_datetime) == month, Booking.id_teacher == id_teacher).all()
    return booking

#TODO: valutare se fare una query per ottenere il prezzo finale delle prentoazione mensili di un insegnante/studente 



@router.get("/test")
def test(db: Session = Depends(get_db)):

    return True
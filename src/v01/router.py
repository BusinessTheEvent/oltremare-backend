from decimal import Decimal
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.auth.models import User
from src.v01.models import Booking, Teacher, TeacherSchoolSubject, Subject, SchoolGrade, AnagSlot, Student
from src.databases.db import get_db
from src.default_logger import get_custom_logger
from src.schemas.v01_schemas import CreateBookingSchema, BookingSchema, FullCalendarBookingSchema, IdSchema, StudentInfoResponse, TeacherInfoResponse, SubjectSchema
from fastapi import HTTPException
from sqlalchemy import extract, or_
from src.config import settings
import datetime
from src.v01 import utils
from sqlalchemy.exc import IntegrityError

from src.default_logger import get_custom_logger

logger = get_custom_logger(__name__)

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
@router.get("/students/all", response_model=list[StudentInfoResponse])
def get_all_students(db: Session = Depends(get_db))->list[StudentInfoResponse]:
    users = db.query(Student).all()
    return users

#accessibile solo da admin
@router.get("/teachers/all", response_model=list[TeacherInfoResponse])
def get_all_teachers(db: Session = Depends(get_db))->list[TeacherInfoResponse]:
    users = db.query(Teacher).all()
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
def get_teacher_by_subject(id_subject: int, id_school_grade: int, db: Session = Depends(get_db)):
    # Query and join to get necessary data
    list = db.query(Teacher, TeacherSchoolSubject, Subject)\
                .join(Teacher, Teacher.id == TeacherSchoolSubject.id)\
                .join(Subject, Subject.id_subject == TeacherSchoolSubject.id_subject)\
                .filter(Subject.id_subject == id_subject, TeacherSchoolSubject.id_school_grade == id_school_grade)\
                .all()

    # Prepare the response in a serializable format
    result = []
    for teacher, teacherSchoolSubject, subject in list:
        teacher_data = {
            'id': teacher.id,
            'name': teacher.user.name,
            'surname': teacher.user.surname,
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
    booking = db.query(Booking).filter(Booking.id_booking == id_booking).first()
    return booking

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
def create_booking(booking_new: CreateBookingSchema , db: Session = Depends(get_db)):    
    ## TODO: add secutiry checks
    ## TODO: make utility function to execute complex query safely

    ## availability check
    available = utils.check_lesson_availability(booking_new, db)

    if available == False:
        logger.info(f"Teacher {booking_new.id_teacher} not available in the selected time slot")
        raise HTTPException(status_code=400, detail="Teacher not available in the selected time slot")

    slots = db.query(AnagSlot).all()

    try:
        duration = (booking_new.end_datetime - booking_new.start_datetime).seconds // 60
        try:
            assert duration > 0, "Duration must be greater than 0"
            assert duration == booking_new.duration, "Duration mismatch"
            assert booking_new.start_datetime >= datetime.datetime.now(), "Start date must be in the future"
            assert booking_new.end_datetime > booking_new.start_datetime, "End date must be after start date"
        except AssertionError as e:
            logger.error(f"Error inserting booking: {e}")
            raise HTTPException(status_code=400, detail="Invalid booking data")

        new_booking = Booking(**booking_new.model_dump(), id_school_grade=utils.get_student_school_grade(booking_new.id_student, db), attended=False, insert_time=datetime.datetime.now().time(), insert_date=datetime.datetime.now().date())

        start_index = utils.hour_to_index(booking_new.start_datetime) 
        end_index = utils.hour_to_index(booking_new.end_datetime) 

        for slot in slots:
            if slot.id_slot >= start_index and slot.id_slot <= end_index:
                new_booking.slots.append(slot)
        
        db.add(new_booking)

        available = utils.check_lesson_availability(booking_new, db)
        
        if not available:
            logger.info(f"One of the users not available in the selected time slot")
            raise HTTPException(status_code=400, detail="Teacher not available in the selected time slot")

        db.commit()

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error inserting booking, booking already exists: {e}")
        raise HTTPException(status_code=409, detail="Booking already exists")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inserting booking: {e}")
        raise HTTPException(status_code=400, detail="Error inserting booking")

    return HTTPException(status_code=200, detail="Booking created successfully")

@router.patch("/booking/update/{id_booking}")
def update_booking(id_booking: int, booking: CreateBookingSchema, db: Session = Depends(get_db)):

    raise HTTPException(status_code=400, detail="Available with Pro Version")

    booking = db.query(Booking).filter(Booking.id_booking == id_booking).first()

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.start_datetime = booking.start_datetime
    booking.end_datetime = booking.end_datetime
    booking.duration = (booking.end_datetime - booking.end_datetime).seconds // 60
    booking.id_student = booking.id_student
    booking.id_teacher = booking.id_teacher
    booking.id_subject = booking.id_subject
    booking.id_school_grade = booking.id_school_grade
    booking.notes = booking.notes
    booking.attended = booking.attended

    db.add(booking)
    db.commit()

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
@router.get("/subjects/all", response_model=list[SubjectSchema])
def get_all_subjects(db: Session = Depends(get_db))-> list[SubjectSchema]:
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

#get booking by month and year per student
@router.get("/booking/get_booking_by_month_and_year/student/{month}/{year}/{id_student}")
def get_booking_by_month_and_year_per_student(month: int, year: int, id_student: int, db: Session = Depends(get_db)):
    # Query and join to get necessary data
    booking = db.query(Booking).filter(extract('month', Booking.start_datetime) == month, extract('year', Booking.start_datetime) == year, Booking.id_student == id_student).all()
    return booking

#get booking by month and year per teacher
@router.get("/booking/get_booking_by_month_and_year/teacher/{month}/{year}/{id_teacher}")
def get_booking_by_month_and_year_per_teacher(month: int, year: int, id_teacher: int, db: Session = Depends(get_db)):
    # Query and join to get necessary data
    booking = db.query(Booking).filter(extract('month', Booking.start_datetime) == month, extract('year', Booking.start_datetime) == year, Booking.id_teacher == id_teacher).all()
    return booking

#get booking by user in fullCalendar format
@router.post("/booking/get_booking_by_user/fullCalendar", response_model=list[FullCalendarBookingSchema])
def get_bookings_by_user_fullCalendar(id_user: IdSchema, db: Session = Depends(get_db)) -> list[FullCalendarBookingSchema]:

    bookings = db.query(Booking).filter(or_(Booking.id_student == id_user.id, Booking.id_teacher == id_user.id )).all()
    print(bookings)
    result = []
    for booking in bookings:
        event = {
            "id_booking": booking.id_booking,
            "start": booking.start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": booking.end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            "title": booking.name,
            "allDay": False
        }
        result.append(event)
        
    return result

#TODO: valutare se fare una query per ottenere il prezzo finale delle prentoazione mensili di un insegnante/studente 

@router.get("/test")
def test(db: Session = Depends(get_db)):

    return True
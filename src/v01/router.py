from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.auth.models import User
from src.v01.models import Booking, Teacher, Student
from src.databases.db import get_db
from src.default_logger import get_custom_logger
from src.schemas.v01_schemas import BookingSchema
from fastapi import HTTPException

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
    booking = db.query(User).filter(User.id == user_id).all()
    return booking

#get all teacher
@router.get("/booking/all_teacher")
def get_all_booking(db: Session = Depends(get_db)):
    return db.query(User,Teacher).join(Teacher, User.id == Teacher.id).all()

#get all teacher groub by subject
@router.get("/booking/all_teacher_by_subject")
def get_all_booking(db: Session = Depends(get_db)):
    return db.query(User,Teacher).join(Teacher, User.id == Teacher.id).all()

#get all student
@router.get("/booking/all_student")
def get_all_booking(db: Session = Depends(get_db)):    
    return db.query(User,Student).join(Student, User.id == Student.id).all()

#accessibile da tutti
@router.get("/booking/{id_booking}")
def get_booking(id_booking: int, db: Session = Depends(get_db)):
    book = db.query(Booking).filter(Booking.id == id_booking).first()
    return book

#prenotazioni di uno studente
@router.get("/booking/{id_student}")
def get_student_booking(id_student: int, db: Session = Depends(get_db)):
    book = db.query(Booking).filter(Booking.id_student == id_student).first()
    return book

#prenotazioni di un insegnante
@router.get("/booking/{id_teacher}")
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
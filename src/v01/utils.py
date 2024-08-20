#controllo 8 lezioni massime in contemporanea in totale
import datetime
from fastapi import Depends, HTTPException
from pytest import Session
from sqlalchemy import text
from src.databases.db import get_db
from src.schemas.v01_schemas import CreateBookingSchema, UpdateUserSchema, TeacherSchoolSubjectSchema, User
from src.v01.models import Message, Subject, Student
from src.default_logger import get_custom_logger

logger = get_custom_logger(__name__)

## TODO: move to environmant variables
START_HOUR = 9
END_HOUR = 18
SLOT_DURATION = 30
SLOTS_IN_HOUR = 60 // SLOT_DURATION

def hour_to_index(hour: datetime.datetime) -> int:
    ## FIXME: check if correct using hour instead of minutes
    return ((hour.hour - START_HOUR) * SLOTS_IN_HOUR + hour.minute // SLOT_DURATION) + 1

def get_user_by_email(email: str, db: Session):
  try:
    user = db.query(User).filter(User.username == email.strip()).first()
  except Exception as e:
    logger.error(f"Error with fetching user from DB: {e}")
    raise HTTPException(status_code=500, detail="Error with fetching user from DB")

  if user is None:
    logger.info(f"User not found with email: {email}")
    raise HTTPException(status_code=404, detail="User not found")
  
  return user

def check_lesson_availability(booking_to_do: CreateBookingSchema, db: Session = Depends(get_db)):

    query = text(f"""
    SELECT a.campo1 AS id_slot, SUM(campo2) AS n_posti_disponibili 
    FROM (
        (
            SELECT id_slot AS campo1, 8 AS campo2 
            FROM anag_slot
            WHERE id_slot NOT IN (
                SELECT DISTINCT bs.id_slot 
                FROM public.booking b 
                JOIN public.booking_slot bs ON b.id_booking = bs.id_booking
                WHERE b.start_datetime >= to_timestamp('{booking_to_do.start_datetime.date()} 00:00:00', 'YYYY-MM-DD HH24:MI:SS') 
                  AND b.start_datetime < to_timestamp('{booking_to_do.start_datetime.date()} 00:00:00', 'YYYY-MM-DD HH24:MI:SS') + interval '1 day'
                  AND (id_student = {booking_to_do.id_student} OR id_teacher = {booking_to_do.id_teacher})
            )
        )
        UNION
        (
            SELECT bs.id_slot, (COUNT(1) * -1) AS campo2 
            FROM public.booking b 
            JOIN public.booking_slot bs ON b.id_booking = bs.id_booking
            WHERE b.start_datetime >= to_timestamp('{booking_to_do.start_datetime.date()} 00:00:00', 'YYYY-MM-DD HH24:MI:SS') 
              AND b.start_datetime < to_timestamp('{booking_to_do.start_datetime.date()} 00:00:00', 'YYYY-MM-DD HH24:MI:SS') + interval '1 day'
            GROUP BY bs.id_slot
        )
    ) a
    GROUP BY a.campo1 
    ORDER BY a.campo1
    """)
    
    query_result = db.execute(query).all()

    result = []
    for row in query_result:
        result.append(row[1])

    start_index = hour_to_index(booking_to_do.start_datetime)
    end_index = hour_to_index(booking_to_do.end_datetime)
    
    for i in range(start_index-1, end_index-1):
        if result[i] <= 0:
            return False

    return True
    

def get_subject_by_name(name: str, db: Session):
    try:
        subject = db.query(Subject).filter(Subject.name == name).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error with fetching subject from DB")

    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    return subject


#get school grade by student id
def get_student_school_grade(student_id: int, db: Session):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error with fetching student from DB")

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student.id_school_grade

#update dei campi username e password di un utente
def update_user(user_id: int, user_new: UpdateUserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    user.username = user_new.username
    user.password = user_new.password
    db.add(user)
    db.commit()
    return user

#send message from user to user
def send_message(sender_id: int, receiver_id: int, message: str, db: Session = Depends(get_db)):
  try:
    logger.info(f"Sending message from user {sender_id} to user {receiver_id}")
    
    new_message = Message(
      id_sender=sender_id,
      id_receiver=receiver_id,
      text=message,
      send_datetime=datetime.datetime.now(),
      is_read=False
    )

    db.add(new_message)
    db.commit()
  except:
    logger.error(f"Error with sending message from user {sender_id} to user {receiver_id}")
    raise HTTPException(status_code=500, detail="Error with sending message")

  return True


# #update delle materie che insegna e a che livello di scuola un insegnante
# def update_teacher_school_subject(teacher_id: int, teacher_new: TeacherSchoolSubjectSchema, db: Session = Depends(get_db)):
#     teacher = db.query(User).filter(User.id == teacher_id).first()
#     teacher.id_school_grade = teacher_new.id_school_grade
#     teacher.teacher_subjects = teacher_new.teacher_subjects
#     db.add(teacher)
#     db.commit()
#     return teacher

  
from decimal import Decimal
import random
from typing import Annotated
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.v01.models import Booking, Message, Teacher, TeacherSchoolSubject, Subject, SchoolGrade, AnagSlot, Student, User, UserOtp
from src.databases.db import get_db
from src.default_logger import get_custom_logger
from src.schemas.v01_schemas import CreateBookingSchema, CreateUserSchema, BookingSchema, EmailSchema, ResetPasswordSchema, FullCalendarBookingSchema, IdSchema, MessageResponse, PreliminaryMeetingSchema, StudentInfoResponse, TeacherInfoResponse, SubjectSchema, UpdateUserSchema, UpdateStudentSchema, UpdateTeacherSchema
from fastapi import HTTPException
from sqlalchemy import extract, or_
from src.config import settings
import datetime
from src.v01 import utils
from sqlalchemy.exc import IntegrityError
from src.schemas import authentication_schemas as auth
from src.default_logger import get_custom_logger
from fastapi import HTTPException
from src.v01.emails import gmail_send_mail_to
import bcrypt

logger = get_custom_logger(__name__)

START_HOUR = 9
END_HOUR = 18
SLOT_DURATION = 30
SLOTS_IN_HOUR = 60 // SLOT_DURATION

FOREWARING_HOURS = 48

SCHOOL_GRADES_DICT = {'Elementari': 1, 'Medie': 2, 'Superiori': 3}
SCHOOL_GRADES_DICT_REVERSE = {1: 'Elementari', 2: 'Medie', 3: 'Superiori'}

router = APIRouter()
logger = get_custom_logger(__name__)

@router.put("/users/register")
def register_user(user: CreateUserSchema, db: Session = Depends(get_db)):

    # Check if the password is strong enough
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    ## hash password
    try:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(user.password.encode('utf-8'), salt).decode('utf-8')
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise HTTPException(status_code=500, detail="Error hashing password")

    # Create a new user
    new_user = User(
        username=user.email,
        name=user.name,
        surname=user.surname,
        birthdate=datetime.datetime.now().date(),
        is_active=True,
        disabled=False,
        additional_scopes="",
        role=2,
        groups=[],
        is_application=False,
        password=password_hash
    )

    db.add(new_user)

    if user.type == "student":
        new_student = Student(user=new_user, id_school_grade=SCHOOL_GRADES_DICT[user.school], preliminary_meeting=False)
        db.add(new_student)
    
    elif user.type == "teacher":
        new_teacher = Teacher(user=new_user)
        db.add(new_teacher)

    else:
        raise HTTPException(status_code=400, detail="Invalid user type")
    
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")

    gmail_send_mail_to(user.email, subject="Registrazione avvenuta con successo", text="La registrazione è avvenuta con successo. Benvenuto su Oltremare!<br>Se non hai svolto tu questa operazione ti preghiamo di ignorare questa email ed eliminarla, grazie.", title="Benvenuto!")

    return

@router.get("/")
def healtcheck():
    return {"status": "ok", "version": settings.APP_VERSION}

#accessibile solo da admin
@router.get("/students/all", response_model=list[StudentInfoResponse])
def get_all_students(db: Session = Depends(get_db))->list[StudentInfoResponse]:
    users = db.query(Student).order_by(Student.id).all()
    return users

#accessibile solo da admin
@router.get("/teachers/all", response_model=list[TeacherInfoResponse])
def get_all_teachers(db: Session = Depends(get_db))->list[TeacherInfoResponse]:
    users = db.query(Teacher).order_by(Teacher.id).all()
    return users

#accessibile solo da admin e insegnante (per gli studenti)
@router.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    return student

#accessibile solo da admin e insegnante (per gli studenti)
@router.get("/teachers/{teacher_id}", response_model=TeacherInfoResponse)
def get_student(teacher_id: int, db: Session = Depends(get_db))->TeacherInfoResponse:
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    return teacher


@router.get("/teachers/subjects/{teacher_id}")
def get_teacher_subjects(teacher_id: int, db: Session = Depends(get_db)):
    # Query and join to get necessary data
    subjects = db.query(TeacherSchoolSubject).filter(TeacherSchoolSubject.id == teacher_id).all()


    """
    {'id_school_grade': 1, 'id': 5, 'id_subject': 1}
    {'id_school_grade': 2, 'id': 5, 'id_subject': 1}
    {'id_school_grade': 1, 'id': 5, 'id_subject': 2}
    {'id_school_grade': 2, 'id': 5, 'id_subject': 2}
    {'id_school_grade': 3, 'id': 5, 'id_subject': 2}
    """


    # Prepare the response in a serializable format
    result = {}
    for subject in subjects:
        result[subject.id_subject] = {}

    for subject in subjects:
        result[subject.id_subject][subject.id_school_grade] = True

    return result


#update dei campi username, password, id_schoolgrade di uno studente
@router.patch("/students/update/{student_id}")
def update_student(student_id: int, student1: UpdateStudentSchema, db: Session = Depends(get_db)):

    if student1.username and db.query(User).filter(User.username.ilike(student1.username)).first():
        raise HTTPException(status_code=409, detail="Username already exists")

    try:
        student = db.query(Student).filter(Student.id == student_id).first()

        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        
        

        student.user.name = student1.name
        student.user.surname = student1.surname
        student.user.username = student1.username if student1.username else student.user.username
        
        if student1.password and student1.password.strip():
            try:
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(student1.password.encode('utf-8'), salt).decode('utf-8')
            except Exception as e:
                logger.error(f"Error hashing password: {e}")
                raise HTTPException(status_code=500, detail="Error hashing password")
            student.user.password = password_hash
            
        student.id_school_grade = student1.id_school_grade

        db.commit()
        
        return {"message": "Student updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating student")
    
@router.patch("/teachers/update/{teacher_id}")
def update_teacher_school_subject(teacher_id: int, teacher1: UpdateTeacherSchema, db: Session = Depends(get_db)):

    if teacher1.username and db.query(User).filter(User.username.ilike(teacher1.username)).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    
    try:
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

        if teacher is None:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        teacher.user.name = teacher1.name
        teacher.user.surname = teacher1.surname
        teacher.user.username = teacher1.username if teacher1.username else teacher.user.username
        if teacher1.password and teacher1.password.strip():
            try:
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(teacher1.password.encode('utf-8'), salt).decode('utf-8')
            except Exception as e:
                logger.error(f"Error hashing password: {e}")
                raise HTTPException(status_code=500, detail="Error hashing password")
            teacher.user.password = password_hash

        # Update the subjects taught by the teacher
        for subject in teacher1.teacher_subjects: # for every checkbox in the frontend list
            subject_id = subject.id
            subject_name = subject.name
            isChecked = subject.isChecked
            levels = subject.levels

            ## if level is not checked, remove it, else add it
            for level in levels:
                teacher_subject_level = db.query(TeacherSchoolSubject).filter(TeacherSchoolSubject.id == teacher_id, TeacherSchoolSubject.id_subject == subject_id, TeacherSchoolSubject.id_school_grade == SCHOOL_GRADES_DICT[level.level]).first()    
                
                if teacher_subject_level is None and level.isChecked:
                    teacher_subject_level = TeacherSchoolSubject(id=teacher_id, id_subject=subject_id, id_school_grade=SCHOOL_GRADES_DICT[level.level])
                    db.add(teacher_subject_level)
                elif teacher_subject_level is not None and not level.isChecked:
                    db.delete(teacher_subject_level)

        db.commit()
        return {"message": "Teacher subjects updated successfully"}
    
    except Exception as e:
        logger.error(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating teacher subjects")

#update dei campi username, password di chief
@router.patch("/users/update/{user_id}")
def update_user(user_id: int, user: UpdateUserSchema, db: Session = Depends(get_db)):

    if user.username and db.query(User).filter(User.username.ilike(user.username)).first():
        raise HTTPException(status_code=409, detail="Username already exists")

    try:
        user_db = db.query(User).filter(User.id == user_id).first()

        if user_db is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_db.name = user.name
        user_db.surname = user.surname
        user_db.username = user.username if user.username else user_db.username
        
        try:
            if user.password and user.password.strip(): ## checks for password to not be None or spaces only
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(user.password.encode('utf-8'), salt).decode('utf-8')
                user_db.password = password_hash
        except Exception as e:
            logger.error(f"Error hashing password: {e}")
        

        db.commit()
        
        return {"message": "User updated successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Error updating user")

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user
    
#verify if the the is the user or not
@router.get("/users/is_teacher/{user_id}")
def get_is_teacher(user_id: int, db: Session = Depends(get_db)):
    # I suppose that if the user isn't a teacher, the only possible type of user is student
    teacher = db.query(Teacher).filter(Teacher.id == user_id).first()
    if teacher:
        return True
    else:
        return False
    

@router.patch("/students/update_preliminary_meeting/{userId}")
def update_preliminary_meeting(userId: int, preliminary_meeting: PreliminaryMeetingSchema, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == userId).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.preliminary_meeting = preliminary_meeting.done

    db.commit()

    return {"message": "Preliminary meeting updated successfully"}
    

#accessibile solo da admin
@router.get("/booking/all")
def get_all_booking(db: Session = Depends(get_db)):
    bookings = db.query(Booking, Teacher).join(Teacher, Booking.id_teacher == Teacher.id).all()
    result = []
    for booking, teacher in bookings:
        result.append({
            'id_booking': booking.id_booking,
            'title': teacher.user.name + " " + teacher.user.surname,
            'start': booking.start_datetime,
            'end': booking.end_datetime,
            'name': booking.name,
            'name_teacher': teacher.user.name,
            'surname_teacher': teacher.user.surname,
            'allDay': "false"
        })
    return result

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
    books = db.query(Booking).filter(Booking.id_student == id_student).order_by(Booking.start_datetime).all()
    return books

#prenotazioni di un insegnante
@router.get("/booking/teacher/{id_teacher}", response_model=list[BookingSchema])
def get_teacher_booking(id_teacher: int, db: Session = Depends(get_db)) -> list[BookingSchema]:
    bookings = db.query(Booking).filter(Booking.id_teacher == id_teacher).order_by(Booking.start_datetime).all()
    return bookings

#accessibile solo da admin e studente
#inserimento di una prenotazione
@router.put("/booking/insert")
def create_booking(booking_new: CreateBookingSchema , db: Session = Depends(get_db)):    
    ## TODO: add secutiry checks
    ## TODO: make utility function to execute complex query safely

    if booking_new.start_datetime.weekday() >=5:
        logger.info(f"Cannot book a lesson on weekends")
        raise HTTPException(status_code=400, detail="Cannot book a lesson on weekends")


    preliminary_meeting = db.query(Student).filter(Student.id == booking_new.id_student).first().preliminary_meeting
    if preliminary_meeting is False:
        raise HTTPException(status_code=403, detail="Preliminary meeting not done")

    if booking_new.start_datetime < datetime.datetime.now() + datetime.timedelta(hours=FOREWARING_HOURS):
        logger.info(f"Cannot book a lesson before FOREWARING_HOURS hours from the start date")
        raise HTTPException(status_code=400, detail="Cannot book a lesson before 72 hours from the start date")

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
            if slot.id_slot >= start_index and slot.id_slot < end_index:
                new_booking.slots.append(slot)
        
        db.add(new_booking)

        available = utils.check_lesson_availability(booking_new, db)
        
        if not available:
            logger.info(f"One of the users not available in the selected time slot")
            raise HTTPException(status_code=400, detail="Teacher not available in the selected time slot",)

        db.commit()

        
        student = db.query(User).filter(User.id == booking_new.id_student).first()
        teacher = db.query(User).filter(User.id == booking_new.id_teacher).first()

        message_to_student = f"{student.name}, la lezione del giorno {booking_new.start_datetime.date()}  alle {booking_new.start_datetime.time().strftime("%H:%M")} è stata aggiunta."
        utils.send_message(teacher.id,student.id, message_to_student, db)
        
        message_to_teacher = f"{teacher.name}, la lezione del giorno {booking_new.start_datetime.date()} alle {booking_new.start_datetime.time().strftime("%H:%M")} è stata aggiunta."
        utils.send_message(student.id,teacher.id, message_to_teacher, db)

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error inserting booking, booking already exists: {e}")
        raise HTTPException(status_code=409, detail="Booking already exists")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inserting booking: {e}")
        raise HTTPException(status_code=400, detail="Error inserting booking")
    
    ## controls for the email event attachment (only premium subscription)
    if settings.ADD_ICS_EVENTS:
        ics_student = utils.generate_ics_file(f"Lezione di {new_booking.subject.name} con {teacher.name}", booking_new.start_datetime, booking_new.end_datetime, location= "Online")
        ics_teacher = utils.generate_ics_file(f"Lezione di {new_booking.subject.name} con {student.name}", booking_new.start_datetime, booking_new.end_datetime, location= "Online")
    else:
        ics_student = None
        ics_teacher = None

    gmail_send_mail_to(student.username,
                       subject="Lezione prenotata",
                       text=f"La lezione di {new_booking.subject.name} è stata prenotata con successo per il giorno {new_booking.start_datetime.date()} alle {new_booking.start_datetime.time().strftime('%H:%M')}.",
                       title="Prenotazione effettuata!",
                       attachment=ics_student,
                       attachment_filename=f"Lezione_{new_booking.subject.name}.ics"
                    )
    
    gmail_send_mail_to(teacher.username,
                       subject="Lezione prenotata",
                       text=f"La lezione di {new_booking.subject.name} è stata prenotata per il giorno {new_booking.start_datetime.date()} alle {new_booking.start_datetime.time().strftime('%H:%M')}.",
                       title="Prenotazione effettuata!",
                       attachment=ics_teacher,
                       attachment_filename=f"Lezione_{new_booking.subject.name}.ics"
                    )

    return HTTPException(status_code=200, detail="Booking created successfully")

@router.patch("/booking/update/{id_booking}")
def update_booking(id_booking: int, booking: CreateBookingSchema, db: Session = Depends(get_db)):

    raise HTTPException(status_code=400, detail="Available with Pro Version")


#rimozione di una prenotazione
@router.delete("/booking/{id_booking}")
def delete_booking(id_booking: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id_booking == id_booking).first()
    subject_name = booking.subject.name
    start_datetime = booking.start_datetime


    today = datetime.datetime.now()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.start_datetime < today:
        raise HTTPException(status_code=400, detail="Cannot delete past bookings")
    
    if booking.start_datetime < today + datetime.timedelta(hours=72):
        raise HTTPException(status_code=400, detail="Cannot delete bookings before 72 hours from the start date")
    
    teacher = db.query(User).filter(User.id == booking.id_teacher).first()
    student = db.query(User).filter(User.id == booking.id_student).first()
    
    # Send message to teacher
    utils.send_message(teacher.id, student.id, f"{student.name}, la lezione del giorno {booking.start_datetime.date()} alle {booking.start_datetime.time().strftime("%H:%M")} è stata cancellata.", db)
    # Send message to student
    utils.send_message(student.id, teacher.id, f"{teacher.name}, la lezione del giorno {booking.start_datetime.date()} alle {booking.start_datetime.time().strftime("%H:%M")} è stata cancellata.", db)

    db.delete(booking)

    ## TODO: implement on cascade?
    db.commit()

    gmail_send_mail_to(student.username, subject="Lezione cancellata", text=f"La lezione di {subject_name} è stata cancellata per il giorno {start_datetime.date()} alle {start_datetime.time().strftime('%H:%M')}.", title="Prenotazione cancellata!")
    gmail_send_mail_to(teacher.username, subject="Lezione cancellata", text=f"La lezione di {subject_name} è stata cancellata per il giorno {start_datetime.date()} alle {start_datetime.time().strftime('%H:%M')}.", title="Prenotazione cancellata!")

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
@router.get("/booking/get_booking_by_month_and_year/student/{month}/{year}/{id_student}", response_model=list[BookingSchema])
def get_booking_by_month_and_year_per_student(month: int, year: int, id_student: int, db: Session = Depends(get_db))->list[BookingSchema]:
    
    # Query and join to get necessary data
    if month == 0 and year == 0:
        #print("no everything")
        booking = db.query(Booking).filter(Booking.id_student == id_student).all()
    elif month == 0:
        #print("no month")
        booking = db.query(Booking).filter(extract('year', Booking.start_datetime) == year, Booking.id_student == id_student).all()
    elif year == 0:
        #print("no year")
        booking = db.query(Booking).filter(extract('month', Booking.start_datetime) == month, Booking.id_student == id_student).all()
    else:
        #print("everything")
        booking = db.query(Booking).filter(extract('month', Booking.start_datetime) == month, extract('year', Booking.start_datetime) == year, Booking.id_student == id_student).all()

    return booking

#get booking by month and year per teacher
@router.get("/booking/get_booking_by_month_and_year/teacher/{month}/{year}/{id_teacher}", response_model=list[BookingSchema])
def get_booking_by_month_and_year_per_teacher(month: int, year: int, id_teacher: int, db: Session = Depends(get_db))->list[BookingSchema]:

    # Query and join to get necessary data
    if month == 0 and year == 0:
        booking = db.query(Booking).filter(Booking.id_teacher == id_teacher).all()
    elif month == 0:
        booking = db.query(Booking).filter(extract('year', Booking.start_datetime) == year, Booking.id_teacher == id_teacher).all()
    elif year == 0:
        booking = db.query(Booking).filter(extract('month', Booking.start_datetime) == month, Booking.id_teacher == id_teacher).all()
    else:
        booking = db.query(Booking).filter(extract('month', Booking.start_datetime) == month, extract('year', Booking.start_datetime) == year, Booking.id_teacher == id_teacher).all()

    return booking

#get booking by user in fullCalendar format
@router.post("/booking/get_booking_by_user/fullCalendar", response_model=list[FullCalendarBookingSchema])
def get_bookings_by_user_fullCalendar(id_user: IdSchema, db: Session = Depends(get_db)) -> list[FullCalendarBookingSchema]:

    bookings = db.query(Booking).filter(or_(Booking.id_student == id_user.id, Booking.id_teacher == id_user.id )).all()
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

#ottenere i messaggi di un utente dove è il ricevente
@router.get("/users/inbox/{id_user}", response_model=list[MessageResponse])
def get_inbox(id_user: int, db: Session = Depends(get_db))->list[MessageResponse]:

    ## TODO: check with auth that user is the receiver

    messages = db.query(Message).filter(Message.id_receiver == id_user, Message.is_read == False).all()
    if messages is None:
        return []
    
    return messages

#update messaggio come letto
@router.patch("/message/update/{id_message}")
def update_message(id_message: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id_message == id_message).first()

    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = True

    db.commit()

    return {"message": "Message updated successfully"}


#update della password di un utente con id user_id
@router.post("/resetpassword")
def reset_password(data: Annotated[ResetPasswordSchema, None], db: Session = Depends(get_db)):
    user_otp = db.query(UserOtp).filter(UserOtp.otp == data.code).first()

    if user_otp is None:
        logger.info(f"OTP {data.code} not found")
        raise HTTPException(status_code=404, detail="OTP not found")
    
    if user_otp.expire_datetime < datetime.datetime.now():
        logger.info(f"OTP {data.code} expired")
        db.delete(user_otp)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")

    user = db.query(User).filter(User.id == user_otp.id_user).first()

    if user is None:
        logger.info(f"User with id {user_otp.id_user} not found")
        db.delete(user_otp)
        db.commit()
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(data.password.encode('utf-8'), salt).decode('utf-8')
        user.password = password_hash

    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise HTTPException(status_code=500, detail="Error hashing password")
    
    finally:
        db.delete(user_otp)
        db.commit()

    return {"message": "Password updated successfully"}



@router.post("/reset_password/otp")
def send_otp(data: Annotated[EmailSchema, None], db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.username == data.email).first()

    if user is None:
        logger.info(f"User with email {data.email} not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    hash = str(random.getrandbits(128).to_bytes(16, 'big').hex())
    message = f"""Per resettare la password clicca il seguente link: <a href="https://doposcuola.martinalucardapsicologa.it/restorePsw?code={hash}">Reset Password</a>. Sarà valido per un'ora."""

    try:
        new_object = UserOtp(id_user=user.id, otp=hash, expire_datetime=datetime.datetime.now() + datetime.timedelta(hours=1))
        db.add(new_object)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error generating OTP: {e}")
        raise HTTPException(status_code=500, detail="Error generating OTP")

    gmail_send_mail_to(data.email, subject="Reset della password", text=message, title="Codice OTP")


@router.get("/test")
def test(db: Session = Depends(get_db)):
    send_otp("riccardo@comellato.name", db)
    return True
#controllo 8 lezioni massime in contemporanea in totale
import datetime
from fastapi import Depends
from pytest import Session
from src.databases.db import get_db
from src.v01.models import Booking


def check_max_lessons(start_datetime: datetime.datetime, end_datetime: datetime.datetime, db: Session = Depends(get_db)):
    # Query and join to get necessary data
    bookings = db.query(Booking).filter(Booking.start_datetime <= start_datetime, Booking.end_datetime >= end_datetime).all()
    return len(bookings) < 8
    
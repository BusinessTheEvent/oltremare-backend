#controllo 8 lezioni massime in contemporanea in totale
import datetime
from fastapi import Depends
from pytest import Session
from sqlalchemy import text
from src.databases.db import get_db
from src.schemas.v01_schemas import CreateBookingSchema

## TODO: move to environmant variables
START_HOUR = 9
END_HOUR = 18
SLOT_DURATION = 30
SLOTS_IN_HOUR = 60 // SLOT_DURATION

def hour_to_index(hour: datetime.datetime) -> int:
    ## FIXME: check if correct using hour instead of minutes
    return ((hour.hour - START_HOUR) * SLOTS_IN_HOUR + hour.minute // SLOT_DURATION) + 1

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
          WHERE b.start_datetime BETWEEN to_timestamp('{booking_to_do.start_datetime.date()} 00:00:00', 'YYYY-MM-DD HH24:MI:SS') 
            AND to_timestamp('{booking_to_do.start_datetime.date()} 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
            AND (id_student = {booking_to_do.id_student} OR id_teacher = {booking_to_do.id_teacher})
        )
      )
      UNION
      (
        SELECT bs.id_slot, (COUNT(1) * -1) AS campo2 
        FROM public.booking b 
        JOIN public.booking_slot bs ON b.id_booking = bs.id_booking
        WHERE b.start_datetime BETWEEN to_timestamp('{booking_to_do.start_datetime.date()} 00:00:00', 'YYYY-MM-DD HH24:MI:SS') 
          AND to_timestamp('{booking_to_do.start_datetime.date()} 23:59:59', 'YYYY-MM-DD HH24:MI:SS')
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
    
    for i in range(start_index-1, end_index):
        if result[i] <= 0:
            return False

    return True
    
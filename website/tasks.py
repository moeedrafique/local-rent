# Celery Task
from celery import shared_task

from main_app.models import Booking


@shared_task
def release_reservation_after_timeout(reservation_id):
    try:
        reservation = Booking.objects.get(id=reservation_id)
        reservation.car.available = True
        reservation.car.save()
        # reservation.delete()
    except Booking.DoesNotExist:
        pass

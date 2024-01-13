# dynamic_schedule.py

from celery.schedules import crontab

# Assuming you have a list_of_reservation_ids from somewhere
list_of_reservation_ids = [1, 2, 3]  # Replace this with your actual reservation IDs

dynamic_schedule = {}

for reservation_id in list_of_reservation_ids:
    task_name = f'check-expired-products-{reservation_id}'
    dynamic_schedule[task_name] = {
        'task': 'website.tasks.release_reservation_after_timeout',
        'schedule': crontab(minute=1, hour=0),  # Adjust the schedule as needed
        'kwargs': {'reservation_id': reservation_id},
    }

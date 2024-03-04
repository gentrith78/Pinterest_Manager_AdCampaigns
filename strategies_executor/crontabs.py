from celery.app import periodic_task
from celery.beat import a
from celery.schedules import crontab
from .tasks import executor

@periodic_task(run_every=crontab(minute='*/10'))
def every_10_minutes_task():
    executor.delay('E10')

@periodic_task(run_every=crontab(minute='*/30'))
def every_30_minutes_task():
    executor.delay('E30')

@periodic_task(run_every=crontab(hour='*'))
def every_hour_task():
    executor.delay('EH')

@periodic_task(run_every=crontab(hour='*/2'))
def every_two_hours_task():
    executor.delay('ETH')

@periodic_task(run_every=crontab(hour=0, minute=0))
def every_day_task():
    executor.delay('ED')

@periodic_task(run_every=crontab(day_of_week='sun', hour=0, minute=0))
def every_week_task():
    executor_task.delay('EW')

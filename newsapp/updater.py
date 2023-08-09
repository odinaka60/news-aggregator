from apscheduler.schedulers.background import BackgroundScheduler
from .update_feed import update_feed_function


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_feed_function, 'interval', minutes=30)
    scheduler.start()
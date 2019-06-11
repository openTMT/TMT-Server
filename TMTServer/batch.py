from apscheduler.schedulers.background import BackgroundScheduler
from iosapp.job import *

sched = BackgroundScheduler()

sched.add_job(update_iOS_device_status, args=(),
              trigger='cron', second='*/2',
              id='update_iOS_device_status', replace_existing=True, misfire_grace_time=15)
# sched.start()

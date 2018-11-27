from apscheduler.schedulers.blocking import BlockingScheduler
from app import handler
import datetime

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=24)
def timed_job():

	formatted_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	print('[Job is running every ~10 minutes]')
	print('[Date : ' + formatted_date + ']')
	handler()
	print('[Timed job finished]')
	print('[Date : ' + formatted_date + ']')

print('[Starting scheduler]')
timed_job()
sched.start()

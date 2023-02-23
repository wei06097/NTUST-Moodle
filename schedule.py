###  schedule.py  ###

MINUTES = 60
from main import checkMoodle
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == '__main__':
    job_defaults = {"max_instances": 100}
    scheduler = BlockingScheduler(timezone="Asia/Taipei", job_defaults=job_defaults)
    scheduler.add_job(checkMoodle, "interval", minutes=MINUTES)
    try:
        print("start mode: continue, interval:", MINUTES, "min")
        scheduler.start()
    except Exception:
        print("scheduler failed")
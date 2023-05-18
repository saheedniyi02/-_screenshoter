from apscheduler.schedulers.blocking import BlockingScheduler
from reply_mentions import reply_mentions,reply_form, clean_replied

scheduler = BlockingScheduler()
scheduler.add_job(reply_mentions, "interval", seconds=30)
scheduler.add_job(clean_replied,"interval",seconds=86400)
scheduler.start()
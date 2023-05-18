from apscheduler.schedulers.background import BackgroundScheduler
from reply_mentions import reply_mentions,reply_form, clean_replied

scheduler = BackgroundScheduler()
scheduler.add_job(func=reply_mentions, trigger="interval", seconds=27)
scheduler.add_job(func=clean_replied,trigger="interval",seconds=86400)
scheduler.start()
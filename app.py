from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from reply_mentions import reply_mentions, clean_replied

app = Flask(__name__)


@app.route("/")
def home():
    return "home"


scheduler = BackgroundScheduler()
scheduler.add_job(func=reply_mentions, trigger="interval", seconds=60)
scheduler.start()


if __name__ == "__main__":
    app.run(debug=False)

import schedule
import time
from datetime import datetime
import mail_logic as ml
import logging

logging.basicConfig(
    filename = 'C:/Users/Administrator/Documents/python_env/email_env/expiry_notifications.log',
    level = logging.INFO,
    format = '%(asctime)s %(levelname)s:%(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)

#schedule.every(0.1).minutes.do(main)
# Scheduling jobs
schedule.every().friday.at("08:00").do(ml.send_monthly_email)  # Weekly for one month
schedule.every().day.at("08:00").do(ml.send_weekly_email)  # Daily for one week
schedule.every().day.at("08:00").do(ml.send_daily_expired_email)  # Twice daily for expired
schedule.every().day.at("16:00").do(ml.send_daily_expired_email)

logging.info("Script started. Beginning scheduled tasks.")
while True:
    schedule.run_pending()
    time.sleep(1)



import schema_def 
import Mongo
import smtplib
import schedule
from dotenv import load_dotenv
import os 
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient
from tkinter import messagebox, Tk
import logging

logging.basicConfig(
    filename = 'expiry_notifications.log',
    level = logging.INFO,
    format = '%(asctime)s %(levelname)s:%(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)

load_dotenv() 

def initial():
    try:     
        #schema_def.ExpiryModelSchemamake_expiry_model()
        connection_string = os.getenv("MONGO_URI")
        database_name = os.getenv("DB_NAME")
        handler = Mongo.MongoDBHandler(connection_string=connection_string, database_name=database_name)
        collection1 = handler.get_expiry_info_collection()
        logging.info("Successfully initialized database connection.")
        return collection1
        # You can use collection1 for further operations
    except Exception as ex:
        logging.error(f"Failed to initialize database: {str(ex)}")
        root = Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror("Error", f"Failed to initialize database: {str(ex)}")
        root.destroy()

def send_mail(subject, body):
    # TODO: change this to handle multiple emails
 
    email_subject = subject 
    email_body = body

    From = "user@email.com"
    password = os.getenv("EMAIL_PASSWORD")
    user_email = ["user1@email.com", "user2@email.com", "user3@email.com"]

    
    message = MIMEMultipart()
    message["From"] = From
    message["To"] = ", ".join(user_email)
    message["Subject"] = subject

    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP("mail.3qs.co.ke", 26) as server:
            server.starttls()
            server.login(From, password)
            server.sendmail(From, user_email, message.as_string())
            logging.info(f"Email sent successfully: {subject}")
            print("Email sent successfully")
        
    except Exception as ex:
        logging.error(f"Failed to send email: {str(ex)}")
        root = Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror("Error", f"Failed to send email: {str(ex)}")
        root.destroy()


def generate_html_email(expiry_type, file_list, total_expired=None):
    if expiry_type == "expired":
        header = f"""<h3 style = " font-family: Garamond;">This is a friendly reminder that the following files have expired:</h3><p style = "font-family: Garamond;"><u>Total expired files: {total_expired}</u></p>"""
    else:
        header = f"""<h3 style = " font-family: Garamond;">This is a friendly reminder that the following files will expire in {expiry_type}:</h3>"""

    file_entries = "".join([f"""<li class = "list-group-item d-flex justify-content-between align-items-center" style = " font-family: Garamond; font-weight: Bold;">{category}</li>""" for category in file_list])

    html_content = f"""
    <html lang = "en">
    <head>
    <meta charset = "utf-8">
    <meta name = "viewport" content = "width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    </head>
    <body>
    <div class = "container-fluid">
    <h2  style = "font-family: Garamond; font-size: 1.2em">Dear Administration Team,<br> </h2>
        {header}
        <ul class = "list-group">
            {file_entries}
        </ul>
        <p style = "font-family: Garamond; font-size: 1.2em">We kindly request that you initiate the process to update this, as soon as possible to remain compliant.<br><br>

Please note that this is an auto-generated email notification from the Bee Tracker Tendering System.<br><br>

Thank you for your attention to this matter. <br><br><br> <b>Sincerely,<br>

Bee Tracker Tendering System<b/></p>
        </div class = "card-header">
        
        <img src = "https://3qs.co.ke/assets/images/logo/bg.png" alt = "3qs logo" width = "100" height = "50"><br>
        <div class = "card-body">
<h4 class = "card-title" style = "font-family: Garamond; font-weight: normal; font-size: 1.2em;" ><br>Phone: +254 787 198 981 </h4>
<p class = "card-text" style = "font-family: Garamond; font-weight: normal">The transmittal and/or attachments are confidential, privileged and proprietary to us or the intended recipient. 
If you are not the intended recipient, you are hereby notified that you have received this transmittal in error and; any review, dissemination, distribution or copying of this transmittal is strictly prohibited. 
You should therefore notify us immediately by reply or by telephone and immediately delete this message and all its attachments. Thank you.</p>
</div>
        <div>

        </div>
    </body>
    </html>
    """

    return html_content

def send_monthly_email():
    current_date = datetime.now()
    collection1 = initial()
    files_expiring_in_month = []
    
    for document in collection1.find({"expires": True}):
        expiry_date = document["expiry_date"]
        days_to_expiry = (expiry_date - current_date).days
        category = document['Category']

        if 0 < days_to_expiry <= 30:
            files_expiring_in_month.append(category)
        
    if files_expiring_in_month:
        subject = "Files Expiring in One Month!!!"
        body = generate_html_email("one month", files_expiring_in_month)
        send_mail(subject, body)
        logging.info("Monthly email sent for files expiring in one month.")

def send_weekly_email():
    current_date = datetime.now()
    collection1 = initial()
    files_expiring_in_week = []
    
    for document in collection1.find({"expires": True}):
        expiry_date = document["expiry_date"]
        days_to_expiry = (expiry_date - current_date).days
        category = document['Category']

        if 0 < days_to_expiry <= 7:
            files_expiring_in_week.append(category)
        
    if files_expiring_in_week:
        subject = "Files Expiring in One Week!!!"
        body = generate_html_email("one week", files_expiring_in_week)
        send_mail(subject, body)
        logging.info("Weekly email sent for files expiring in one week.")

def send_daily_expired_email():
    current_date = datetime.now()
    collection1 = initial()
    expired_files = []
    
    for document in collection1.find({"expires": True}):
        expiry_date = document["expiry_date"]
        days_to_expiry = (expiry_date - current_date).days
        category = document['Category']

        if days_to_expiry < 0:
            expired_files.append(category)
        
    if expired_files:
        subject = "Expired Files Notification!!!"
        body = generate_html_email("expired", expired_files, len(expired_files))
        send_mail(subject, body)
        logging.info("Daily email sent for expired files.")

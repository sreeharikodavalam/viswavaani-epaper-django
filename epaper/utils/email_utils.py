import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import environ

env = environ.Env()
environ.Env.read_env()


def send_verification_mail(url, name):
    pass


def send_email(to_addr, subject, body, attachment_path=None):
    smtp_server = env('SMTP_SERVER')
    smtp_port = env('SMTP_PORT')
    username = env('SMTP_USERNAME')
    password = env('SMTP_PASSWORD')
    from_addr = env('SMTP_USER_FROM_MAIL')
    # ---------------------------------
    message = MIMEMultipart()
    message['From'] = from_addr
    message['To'] = to_addr
    message['Subject'] = subject

    # Attach the body with the msg instance
    message.attach(MIMEText(body, 'plain'))

    # Attach the file (optional)
    if attachment_path:
        attachment = open(attachment_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
        message.attach(part)

    # Create SMTP session for sending the mail
    try:
        session = smtplib.SMTP(smtp_server, smtp_port)  # use gmail with port
        session.starttls()  # enable security
        session.login(username, password)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(from_addr, to_addr, text)
        session.quit()
        print(f'Mail Sent to {to_addr}')
    except Exception as e:
        print(f'Failed to send email. Error: {e}')

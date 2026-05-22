import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_ADDRESS = "doorlockofficial1@gmail.com"

EMAIL_PASSWORD = "hnzzbbmovhdcozkc"


def send_order_email(
  to_email: str,
  order_id: int
):

    try:

      subject = "DoorLock Shop Order"

      body = f"""
        Thank you for your order!

        Order ID: {order_id}

        DoorLock Shop
        """

      msg = MIMEMultipart()

      msg["From"] = EMAIL_ADDRESS
      msg["To"] = to_email
      msg["Subject"] = subject

      msg.attach(
        MIMEText(body, "plain")
      )

      server = smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
      )

      server.starttls()

      server.login(
        EMAIL_ADDRESS,
        EMAIL_PASSWORD
      )

      server.send_message(msg)

      server.quit()

      print("EMAIL SENT SUCCESS")

    except Exception as e:
      print("EMAIL ERROR:", e)

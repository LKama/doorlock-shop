from fastapi_mail import (
  FastMail,
  MessageSchema,
  ConnectionConfig
)

conf = ConnectionConfig(
  MAIL_USERNAME="doorlockofficial1@gmail.com",
  MAIL_PASSWORD="hnzzbbmovhdcozkc",
  MAIL_FROM="doorlockofficial1@gmail.com",
  MAIL_PORT="587",
  MAIL_SERVER="smtp.gmail.com",
  MAIL_STARTTLS=True,
  MAIL_SSL_TLS=False,
  USE_CREDENTIALS=True,
  VALIDATE_CERTS=True
)

async def send_order_email(
    email: str,
    order_id: int
):
  message = MessageSchema(
    subject="DoorLock Shop Order",
    recipients=[email],
    body=f"""
    Thank you for your order!

    Order ID: {order_id}
    """,
    subtype="plain"
  )

  fm = FastMail(conf)

  await fm.send_message(message)
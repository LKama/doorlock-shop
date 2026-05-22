import resend

resend.api_key = "re_8jd3HPPn_67BihZjCwjY2PGLD8Vjrydso"


def send_order_email(
  to_email: str,
  order_id: int
):

  try:

    params = {

      "from":
        "DoorLock Shop <onboarding@resend.dev>",

      "to": [to_email],

      "subject":
        "DoorLock Shop Order",

      "html": f"""
        <h1>Thank you for your order!</h1>

        <p>Order ID: {order_id}</p>
      """
    }

    resend.Emails.send(params)

    print("EMAIL SENT SUCCESS")

  except Exception as e:
    print("EMAIL ERROR:", e)
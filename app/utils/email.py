import resend

resend.api_key = "ТВОЙ_RESEND_API_KEY"


def send_order_email(
  user_email,
  order_id,
  address,
  phone,
  products,
  total
):

  try:

      html = f"""
      <h1>DoorLock Shop</h1>

      <h2>New Order #{order_id}</h2>

      <p><b>Customer Email:</b> {user_email}</p>

      <p><b>Phone:</b> {phone}</p>

      <p><b>Address:</b> {address}</p>

      <hr>

      <h2>Products</h2>
      """

      for product in products:

        html += f"""
        <div style="margin-bottom:20px">

          <img
            src="{product['image_url']}"
            width="150"
          >

          <p>
            <b>{product['name']}</b>
          </p>

          <p>
            Quantity: {product['quantity']}
          </p>

          <p>
            Price: {product['price']} ₽
          </p>

        </div>
        """

      html += f"""
      <hr>

      <h2>Total: {total} ₽</h2>
      """

      params = {

        "from":
          "DoorLock Shop <onboarding@resend.dev>",

        "to":
          ["doorlockofficial1@gmail.com"],

        "subject":
          f"New Order #{order_id}",

        "html":
          html
      }

      resend.Emails.send(params)

      print("EMAIL SENT SUCCESS")

  except Exception as e:

    print("EMAIL ERROR:", e)
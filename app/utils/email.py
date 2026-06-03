import resend

resend.api_key = "re_8jd3HPPn_67BihZjCwjY2PGLD8Vjrydso"


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

      <h2>Новый заказ №{order_id}</h2>

      <p><b>Email клиента:</b> {user_email}</p>

      <p><b>Телефон:</b> {phone}</p>

      <p><b>Адрес доставки:</b> {address}</p>

      <hr>

      <h2>Товары</h2>
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
          Количество: {product['quantity']}
        </p>

        <p>
          Цена: {product['price']} ₽
        </p>

      </div>
      """

    html += f"""
    <hr>

    <h2>Итого: {total} ₽</h2>
    """

    params = {

      "from": "DoorLock Shop <onboarding@resend.dev>",

      "to":
        ["lord.kam.2006@gmail.com"],

      "subject": f"Order #{order_id}",

      "html":
        html
    }

    resend.Emails.send(params)

    print("EMAIL SENT SUCCESS")

  except Exception as e:

    print("EMAIL ERROR:", e)
import requests
from django.conf import settings
import uuid
import os

def create_cashfree_order(order_id,order_amount,costomer_username,coostomer_mail,customer_phone):
    url = "https://test.cashfree.com/api/v1/order/create"

    payload = {
        "appId": os.getenv("APP_ID"),  # Replace with your actual app ID
        "secretKey":  os.getenv("SECRET_TEST"),  # Replace with your actual secret key
        "orderId": order_id,  # Replace with your order ID
        "orderAmount": order_amount,  # Replace with your order amount
        "orderCurrency": "INR",
        "orderNote": "this is an optional field",  # Replace with your order note
        "customerName": costomer_username,  # Replace with customer name
        "customerEmail": coostomer_mail,  # Replace with customer email
        "customerPhone": customer_phone,  # Replace with customer phone number
        "returnUrl": "https://f491-2409-40d4-306f-4d38-d4ee-a60b-a5c8-a171.ngrok-free.app/payment-success/",  # ✅ Redirect User Here
        "notifyUrl": "https://f491-2409-40d4-306f-4d38-d4ee-a60b-a5c8-a171.ngrok-free.app/cashfree_webhook/" # Replace with your notify URL if any
    }
    # "returnUrl": "https://www.cashfree.com/",  # Replace with your return URL
    # "notifyUrl": ""

    try:
        response = requests.request("POST",url, data=payload)


        print(response.text)
        # print(order_id)

        try:
            response_json = response.json()
            payment_url = response_json.get("paymentLink")
            print(payment_url)
            return payment_url, {"order_id": order_id, "status": "Order Created Successfully"}
        except (KeyError, ValueError):
            print("Failed to fetch payment URL")
            return None, None
    except Exception as e:
        return print({"error": str(e)})


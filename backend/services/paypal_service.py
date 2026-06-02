import os
import requests
from flask import current_app


def get_paypal_base_url():
    """Trả về base URL của PayPal API dựa theo mode (sandbox/live)"""

    mode = os.getenv("PAYPAL_MODE", "sandbox")

    if mode == "live":
        return "https://api-m.paypal.com"

    return "https://api-m.sandbox.paypal.com"


def get_paypal_access_token():
    """Lấy access token từ PayPal bằng Client Credentials"""

    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
    base_url = get_paypal_base_url()

    response = requests.post(
        f"{base_url}/v1/oauth2/token",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US"
        },
        data={
            "grant_type": "client_credentials"
        },
        auth=(client_id, client_secret)
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to get PayPal access token: {response.text}"
        )

    return response.json()["access_token"]


def create_paypal_order(amount_usd, description="G4 ToyStore Order"):
    """
    Tạo đơn hàng PayPal.
    - amount_usd: Số tiền USD (đã quy đổi từ VND)
    - description: Mô tả đơn hàng
    - Trả về order data bao gồm order ID và approval URL
    """

    access_token = get_paypal_access_token()
    base_url = get_paypal_base_url()

    order_payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": str(round(amount_usd, 2))
                },
                "description": description
            }
        ],
        "application_context": {
            "brand_name": "G4 ToyStore",
            "landing_page": "NO_PREFERENCE",
            "user_action": "PAY_NOW",
            "return_url": "http://localhost:5000/api/paypal/success",
            "cancel_url": "http://localhost:5000/api/paypal/cancel"
        }
    }

    response = requests.post(
        f"{base_url}/v2/checkout/orders",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        json=order_payload
    )

    if response.status_code not in [200, 201]:
        raise Exception(
            f"Failed to create PayPal order: {response.text}"
        )

    return response.json()


def capture_paypal_order(order_id):
    """
    Capture (xác nhận thanh toán) cho đơn hàng PayPal.
    - order_id: ID đơn hàng PayPal đã được approve bởi người dùng
    - Trả về thông tin thanh toán đã hoàn tất
    """

    access_token = get_paypal_access_token()
    base_url = get_paypal_base_url()

    response = requests.post(
        f"{base_url}/v2/checkout/orders/{order_id}/capture",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    )

    if response.status_code not in [200, 201]:
        raise Exception(
            f"Failed to capture PayPal order: {response.text}"
        )

    return response.json()

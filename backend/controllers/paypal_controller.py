from flask import request

from services.paypal_service import create_paypal_order
from services.paypal_service import capture_paypal_order

from utils.response import success_response
from utils.response import error_response


# Tỷ giá cố định VND -> USD
VND_TO_USD_RATE = 25000


def create_order():
    """
    Tạo đơn hàng PayPal từ thông tin sản phẩm.
    Body JSON cần có:
    - product_name: Tên sản phẩm
    - quantity: Số lượng
    - price_vnd: Giá sản phẩm (VND, dạng số)
    """

    try:
        data = request.get_json()

        if not data:
            return error_response(
                "Missing request body",
                400
            )

        product_name = data.get("product_name", "Sản phẩm G4")
        quantity = int(data.get("quantity", 1))
        price_vnd = float(data.get("price_vnd", 0))

        if price_vnd <= 0:
            return error_response(
                "Invalid product price",
                400
            )

        # Tính tổng tiền VND và quy đổi sang USD
        total_vnd = price_vnd * quantity
        total_usd = total_vnd / VND_TO_USD_RATE

        # Đảm bảo tối thiểu 0.01 USD
        if total_usd < 0.01:
            total_usd = 0.01

        description = f"{product_name} x{quantity} - G4 ToyStore"

        # Gọi PayPal service để tạo đơn hàng
        order_data = create_paypal_order(
            amount_usd=total_usd,
            description=description
        )

        return success_response(
            "PayPal order created successfully",
            {
                "order_id": order_data["id"],
                "total_vnd": total_vnd,
                "total_usd": round(total_usd, 2),
                "status": order_data["status"]
            }
        )

    except Exception as e:

        return error_response(
            f"Failed to create PayPal order: {str(e)}",
            500
        )


def capture_order():
    """
    Capture (xác nhận thanh toán) đơn hàng PayPal.
    Body JSON cần có:
    - order_id: PayPal Order ID
    """

    try:
        data = request.get_json()

        if not data or not data.get("order_id"):
            return error_response(
                "Missing order_id",
                400
            )

        order_id = data["order_id"]

        # Gọi PayPal service để capture payment
        capture_data = capture_paypal_order(order_id)

        # Lấy thông tin từ capture response
        payer = capture_data.get("payer", {})
        purchase_unit = capture_data.get(
            "purchase_units", [{}]
        )[0]

        capture_info = purchase_unit.get(
            "payments", {}
        ).get("captures", [{}])[0]

        return success_response(
            "Payment captured successfully",
            {
                "transaction_id": capture_info.get("id"),
                "order_id": capture_data.get("id"),
                "status": capture_data.get("status"),
                "payer_email": payer.get(
                    "email_address", ""
                ),
                "payer_name": payer.get(
                    "name", {}
                ).get("given_name", ""),
                "amount": capture_info.get(
                    "amount", {}
                ).get("value", "0"),
                "currency": capture_info.get(
                    "amount", {}
                ).get("currency_code", "USD")
            }
        )

    except Exception as e:

        return error_response(
            f"Failed to capture PayPal payment: {str(e)}",
            500
        )

import random


def validate_payment(payment: dict) -> tuple[bool, str]:
    """
    Validate that the required fields are present
    based on the payment mode.
    """
    mode = payment.get("payment_mode", "")

    # normalize payment mode to handle case-insensitive input
    mode_mapping = {
        "upi": "UPI",
        "credit card": "Credit Card",
        "wallet": "Wallet",
    }
    mode = mode_mapping.get(mode.lower(), mode)
    payment["payment_mode"] = mode

    if mode == "UPI":
        if not payment.get("upi_id"):
            return False, "Missing required field: upi_id for UPI payment"
    elif mode == "Credit Card":
        missing = []
        for field in ["card_number", "expiry", "cvv"]:
            if not payment.get(field):
                missing.append(field)
        if missing:
            return False, f"Missing required fields for Credit Card: {', '.join(missing)}"
    elif mode == "Wallet":
        if not payment.get("wallet_id"):
            return False, "Missing required field: wallet_id for Wallet payment"
    else:
        return False, f"Unsupported payment mode: {mode}"

    return True, "Validation passed"


def process_payment(payment: dict) -> dict:
    """
    Process the payment after validation.
    Simulates a ~20% random failure rate.
    """
    valid, message = validate_payment(payment)
    if not valid:
        return {"success": False, "message": message}

    # simulate random payment failure
    if random.random() < 0.2:
        return {
            "success": False,
            "message": f"Payment failed via {payment['payment_mode']}. Please try again.",
        }

    return {
        "success": True,
        "message": f"Payment successful via {payment['payment_mode']}",
    }

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class SeatResponse(BaseModel):
    seat_id: str
    available: bool


class PaymentInfo(BaseModel):
    payment_mode: str = Field(..., min_length=1)
    upi_id: Optional[str] = None
    card_number: Optional[str] = None
    expiry: Optional[str] = None
    cvv: Optional[str] = None
    wallet_id: Optional[str] = None


class BookingRequest(BaseModel):
    user: str = Field(..., min_length=1)
    seat_id: str = Field(..., min_length=1)
    payment: PaymentInfo

    @field_validator("user")
    @classmethod
    def user_must_not_be_blank(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("User name cannot be empty or whitespace")
        return stripped


class BookingResponse(BaseModel):
    booking_id: str
    seat_id: str
    status: str


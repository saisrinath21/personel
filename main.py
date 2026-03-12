from fastapi import FastAPI, HTTPException
from models import SeatResponse, BookingRequest, BookingResponse
from payment import process_payment
import store

app = FastAPI(
    title="Dhurandhar Movie Ticket Booking API",
    description="Backend service for booking tickets for the movie Dhurandhar",
    version="1.0.0",
)


@app.get("/seats/{seat_id}", response_model=SeatResponse)
async def check_seat(seat_id: str):
    """Check if a specific seat is available."""
    seat_id = seat_id.upper()

    if seat_id not in store.seats:
        raise HTTPException(status_code=404, detail=f"Seat {seat_id} does not exist")

    return SeatResponse(seat_id=seat_id, available=store.seats[seat_id])


@app.post("/book", response_model=BookingResponse)
async def book_ticket(request: BookingRequest):
    """Book a ticket for the given seat with payment processing."""
    seat_id = request.seat_id.upper()

    # check if seat exists
    if seat_id not in store.seats:
        raise HTTPException(status_code=404, detail=f"Seat {seat_id} does not exist")

    # acquire per-seat lock to prevent concurrent double bookings
    async with store.seat_locks[seat_id]:

        # check availability inside the lock
        if not store.seats[seat_id]:
            raise HTTPException(
                status_code=409,
                detail=f"Seat {seat_id} is already booked",
            )

        # process payment
        payment_result = process_payment(request.payment.model_dump())

        if not payment_result["success"]:
            # payment failed → seat stays available
            raise HTTPException(
                status_code=402,
                detail=payment_result["message"],
            )

        # payment succeeded → mark seat as booked
        store.seats[seat_id] = False

        booking_id = f"B{store.booking_counter}"
        store.booking_counter += 1

        booking = {
            "booking_id": booking_id,
            "user": request.user,
            "seat_id": seat_id,
            "payment_mode": request.payment.payment_mode,
            "status": "CONFIRMED",
        }
        store.bookings.append(booking)

    return BookingResponse(
        booking_id=booking_id,
        seat_id=seat_id,
        status="CONFIRMED",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)

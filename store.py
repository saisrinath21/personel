import asyncio

# ──────────────────────────────────────────────
# In-memory seat map: A1-A20 and B1-B20
# All seats start as available
# ──────────────────────────────────────────────

seats: dict[str, bool] = {}

for row in ["A", "B"]:
    for num in range(1, 21):
        seat_id = f"{row}{num}"
        seats[seat_id] = True  # True = available

# ──────────────────────────────────────────────
# Booking storage
# ──────────────────────────────────────────────

bookings: list[dict] = []
booking_counter: int = 101  # booking IDs start at B101

# ──────────────────────────────────────────────
# Per-seat locks for handling concurrent bookings
# ──────────────────────────────────────────────

seat_locks: dict[str, asyncio.Lock] = {
    seat_id: asyncio.Lock() for seat_id in seats
}

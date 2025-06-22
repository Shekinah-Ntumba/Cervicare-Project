from fastapi import APIRouter
from datetime import datetime, timedelta

router = APIRouter(prefix="/screening", tags=["Screening"])

@router.get("/book")
def book_screening():
    # Example: suggest next available slot
    next_slot = datetime.now() + timedelta(days=3)
    return {
        "message": "Book your screening appointment.",
        "next_available_date": next_slot.strftime("%Y-%m-%d"),
        "booking_link": "https://example-screening.com/booking"
    }

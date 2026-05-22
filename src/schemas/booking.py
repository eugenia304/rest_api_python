from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class BookingDates(BaseModel):
    """
    checkin and checkout fields

    the validator explicitly checks that the checkin > checkout in the client request
    there is a bug in the system and there is no actual validation on this
    """
    model_config = ConfigDict(extra="forbid")

    checkin: date
    checkout: date

    @model_validator(mode="after")
    def validate_date_order(self) -> "BookingDates":
        """Ensures that the checkout date happens after or on the checkin date."""
        if self.checkout < self.checkin:
            raise ValueError("checkout date cannot be before checkin date")
        return self


class Booking(BaseModel):
    """
    Full booking details
    """
    model_config = ConfigDict(extra="forbid")

    firstname: str = Field(..., min_length=1)
    lastname: str = Field(..., min_length=1)
    totalprice: int = Field(..., gt=0)
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None


# -------------------------
# CREATE BOOKING
# -------------------------

class BookingIdItem(BaseModel):
    """A single item returned by GET /booking"""
    bookingid: int


class CreateBookingResponse(BaseModel):
    """Structure returned by POST /booking"""
    model_config = ConfigDict(extra="forbid")

    bookingid: int
    booking: Booking

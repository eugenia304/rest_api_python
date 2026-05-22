from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class BookingDates(BaseModel):
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
    """Represents a single item returned by GET /booking (List)"""
    bookingid: int


class CreateBookingResponse(BaseModel):
    """Represents the wrapping structure returned by POST /booking"""
    model_config = ConfigDict(extra="forbid")

    bookingid: int
    booking: Booking


class APIErrorResponse(BaseModel):
    """
    Standard structure for bad inputs. 
    Note: Restful-Booker often returns strings, but standard APIs use objects.
    """
    model_config = ConfigDict(extra="forbid")

    error: str
    message: Optional[str] = None

import pytest

from datetime import datetime, timedelta
from time import time
from pydantic import TypeAdapter

from schemas.booking import BookingIdItem, Booking, CreateBookingResponse


"""
Validating schemas for the following responses:
    - GET /booking
    - GET /booking/:id
    - POST /booking
    - PUT /booking/:id
    - PATCH /booking/:id
    - DELETE /booking/:id
"""


class TestBookingSchemas:

    def test_schema_get_all_bookings(self, api_client):
        response = api_client.get("/booking")
        assert response.status_code == 200

        # Validates that the response is a clean list of {'bookingid': int} items
        adapter = TypeAdapter(list[BookingIdItem])
        validated_list = adapter.validate_python(response.json())

        assert len(validated_list) > 0

    def test_schema_get_booking_by_id(self, api_client, unique_booking):
        target_id = unique_booking["id"]
        expected_data = unique_booking["data"]

        response = api_client.get(f"/booking/{target_id}")
        assert response.status_code == 200

        validated_response = Booking.model_validate(response.json())
        assert validated_response.firstname == expected_data['firstname']

    def test_schema_post_booking(self, api_client):
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

        payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLastname-{unique_suffix}",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {
                "checkin": date_start,
                "checkout": date_end
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        response = api_client.post("/booking", json=payload)
        assert response.status_code == 200

        validated_response = CreateBookingResponse.model_validate(
            response.json())
        assert validated_response.booking.firstname == payload['firstname']

    def test_schema_put_booking(self, api_client, auth_token, unique_booking):
        target_id = unique_booking["id"]
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d")

        updated_payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLastname-{unique_suffix}",
            "totalprice": 350,
            "depositpaid": False,
            "bookingdates": {
                "checkin": date_start,
                "checkout": date_end
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 200

        validated_response = Booking.model_validate(response.json())

        # Converting response to dict
        validated_dict = validated_response.model_dump()

        assert validated_dict['firstname'] == updated_payload['firstname']
        assert validated_dict['lastname'] == updated_payload['lastname']
        assert validated_dict['totalprice'] == updated_payload['totalprice']
        assert validated_dict['depositpaid'] == updated_payload['depositpaid']
        assert validated_dict['additionalneeds'] == updated_payload['additionalneeds']
        assert validated_dict['bookingdates']['checkin'].strftime(
            '%Y-%m-%d') == updated_payload['bookingdates']['checkin']
        assert validated_dict['bookingdates']['checkout'].strftime(
            '%Y-%m-%d') == updated_payload['bookingdates']['checkout']

    def test_schema_patch_booking(self, api_client, auth_token, unique_booking):
        target_id = unique_booking["id"]
        orig_data = unique_booking["data"]
        unique_suffix = str(int(time()))

        updated_payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.patch(f"/booking/{target_id}",
                                    json=updated_payload, headers=headers)
        assert response.status_code == 200

        validated_response = Booking.model_validate(response.json())

        # Converting response to dict
        validated_dict = validated_response.model_dump()

        assert validated_dict['firstname'] == updated_payload['firstname']
        assert validated_dict['lastname'] == orig_data['lastname']
        assert validated_dict['totalprice'] == orig_data['totalprice']
        assert validated_dict['depositpaid'] == orig_data['depositpaid']
        assert validated_dict['bookingdates']['checkin'].strftime(
            '%Y-%m-%d') == orig_data['bookingdates']['checkin']
        assert validated_dict['bookingdates']['checkout'].strftime(
            '%Y-%m-%d') == orig_data['bookingdates']['checkout']

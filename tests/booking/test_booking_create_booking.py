import pytest

from datetime import datetime, timedelta
from time import time


"""
Booking should have the following format:
{
    'firstname': 'Firstname', 
    'lastname': 'Lastname', 
    'totalprice': 250, 
    'depositpaid': True, 
    'bookingdates': {
        'checkin': 'YYYY-MM-DD', 
        'checkout': 'YYYY-MM-DD'
        }, 
    'additionalneeds': 'Additional Needs'
}

Test cases:
    Valid request:
        - Create booking by providing valid values for all fields
        - Long string (>1000 chars)
        - Idempotency check: send the same payload twice to verify that they get different booking ids
    Negative:
        - Missing one field
        - None value for one field
        - Invalid value type for one field
        - Zero/negative totalprice
        - Checkout date < Checkin date
        - Empty string as the string field value        
"""


class TestCreateValidBooking:

    def test_post_create_booking_valid(self, api_client):
        """
        Valid POST request

        Expected result:
            - status code = 200
        """
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

        payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLasname-{unique_suffix}",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {
                "checkin": date_start,
                "checkout": date_end
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        response = api_client.post("/booking", json=payload)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

    @pytest.mark.parametrize('field_name', [
        'firstname',
        'lastname',
        'additionalneeds'
    ])
    def test_post_create_booking_long_str(self, api_client, field_name):
        """
        Long value (1000 symbols) specified for a string field

        Expected result:
            - status code = 200
        """
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

        payload = {
            "firstname": f"TestLasname-{unique_suffix}",
            "lastname": f"TestLasname-{unique_suffix}",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {
                "checkin": date_start,
                "checkout": date_end
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        payload[field_name] = 'A' * 1000

        response = api_client.post("/booking", json=payload)
        assert response.status_code == 200, (
            f'Request failed with 1000 chars for {field_name} value.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    def test_post_create_booking_same_request_sent_twice(self, api_client):
        """
        Send the same request twice to verify that 2 entries created

        Expected result for both requests:
            - status code = 200
            - id1 != id2
        """
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

        payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLasname-{unique_suffix}",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {
                "checkin": date_start,
                "checkout": date_end
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        response_one = api_client.post(
            "/booking", json=payload)
        assert response_one.status_code == 200, f'Expecting status code 200, got {response_one.status_code}'
        id_one = response_one.json().get("bookingid")

        response_two = api_client.post(
            "/booking", json=payload)
        assert response_two.status_code == 200, f'Expecting status code 200, got {response_two.status_code}'
        id_two = response_two.json().get("bookingid")

        assert id_one != id_two, (
            f"POST /booking is behaving idempotently.\n"
            f"Both requests generated the same booking ID: {id_one}"
        )


class TestCreateBookingNegative:

    @pytest.mark.parametrize('missing_fld', [
        'firstname',
        'lastname',
        'totalprice',
        'depositpaid',
        'bookingdates',
    ])
    def test_post_create_booking_missing_fld(self, api_client, missing_fld):
        """
        Create booking with missing field

        !!! additionalnotes field is optional

        Expected result:
            - status code = 400
        """
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

        payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLasname-{unique_suffix}",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {
                "checkin": date_start,
                "checkout": date_end
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        payload.pop(missing_fld)

        response = api_client.post("/booking", json=payload)

        try:
            assert response.status_code == 400, f'Expecting status code 400, got {response.status_code}'
        except AssertionError as exc:
            if response.status_code == 500:
                pytest.xfail(
                    f'Known bug: status code == 500 instead of 400 for {missing_fld}')
            elif response.status_code in [200, 201]:
                raise AssertionError(
                    f'Request unexpectedly accepted with the missing field {missing_fld}.')

    @pytest.mark.parametrize('null_fld', [
        'firstname',
        'lastname',
        'totalprice',
        'depositpaid',
        'bookingdates'
    ])
    def test_post_create_booking_null_value(self, api_client, null_fld):
        """
        Create booking with null value (None) for a field

        Expected result:
            - status code = 400
        """
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

        payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLasname-{unique_suffix}",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {
                "checkin": date_start,
                "checkout": date_end
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        payload[null_fld] = None

        response = api_client.post("/booking", json=payload)

        try:
            assert response.status_code == 400, f'Expecting status code 400, got {response.status_code}'
        except AssertionError as exc:
            if response.status_code == 500:
                pytest.xfail(
                    f'Known bug: status code == 500 instead of 400 for {null_fld}')
            elif response.status_code in [200, 201]:
                raise AssertionError(
                    f'Request unexpectedly accepted with the None value for {null_fld}.')

    @pytest.mark.parametrize('field_name, invalid_value', [
        ('firstname', 12345),
        ('lastname', True),
        ('bookingdates', '2026-12-03'),
        ("depositpaid", "no")
    ])
    def test_post_create_booking_invalid_value_type(self, api_client, field_name, invalid_value):
        """
        Create booking with invalid type value for a field

        Expected result:
            - status code = 400
        """
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

        payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLasname-{unique_suffix}",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {
                "checkin": date_start,
                "checkout": date_end
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        payload[field_name] = invalid_value

        response = api_client.post("/booking", json=payload)

        try:
            assert response.status_code == 400, f'Expecting status code 400, got {response.status_code}'
        except AssertionError as exc:
            if response.status_code == 500:
                pytest.xfail(
                    f'Known bug: status code == 500 instead of 400 for {field_name}')
            elif response.status_code in [200, 201]:
                raise AssertionError(
                    f'Request unexpectedly accepted with the invalid value type {type(invalid_value)} for {field_name}.')
            else:
                raise AssertionError(
                    f'Unexpected status code {response.status_code}')

    @pytest.mark.parametrize('totalprice', [0, -1, 100.0, 'one'])
    @pytest.mark.xfail(reason='no validation on totalprice field value')
    def test_post_create_booking_totalprice(self, api_client, totalprice):
        """
        Invalid total price specified

        Expected result:
            status code != 200 (not documented)
        """
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

        payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLasname-{unique_suffix}",
            "totalprice": totalprice,
            "depositpaid": True,
            "bookingdates": {
                "checkin": date_start,
                "checkout": date_end
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        response = api_client.post("/booking", json=payload)
        assert response.status_code != 200, (
            f'Request unexpectedly accepted with {totalprice} value for a totalprice.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    @pytest.mark.xfail(reason='checkin > checkout is accepted')
    def test_post_create_booking_checkin_checkout(self, api_client):
        """
        Checkin date > checkout date

        Expected result:
            - status code != 200 (not documented)
        """
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

        payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLasname-{unique_suffix}",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {
                "checkin": date_end,
                "checkout": date_start
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        response = api_client.post("/booking", json=payload)
        assert response.status_code != 200, (
            f'Request unexpectedly accepted with checkin > checkout.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    @pytest.mark.parametrize('field_name', [
        'firstname',
        'lastname',
    ])
    @pytest.mark.xfail(reason='Empty string accepted as a value')
    def test_post_create_booking_empty_str(self, api_client, field_name):
        """
        Empty value sent for a string field

        Expected result:
            - status code = 400
        """
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

        payload = {
            "firstname": f"TestLasname-{unique_suffix}",
            "lastname": f"TestLasname-{unique_suffix}",
            "totalprice": 250,
            "depositpaid": True,
            "bookingdates": {
                "checkin": date_start,
                "checkout": date_end
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        payload[field_name] = ''

        response = api_client.post("/booking", json=payload)
        assert response.status_code == 400, (
            f'Request unexpectedly accepted with the empty field {field_name}.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

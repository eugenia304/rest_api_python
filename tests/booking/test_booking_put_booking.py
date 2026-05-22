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
        - All fields specified and have new values
        - All fields specified but some have original values
        - All fields specified and have original values
        - One of the fields not specified in the request
        - Idempotency check: send the same payload twice
        - Long string (>1000 chars)
    Negative:
        - NULL value for a field
        - Empty string as the string field value
        - Zero/negative price
        - Checkout date < Checkin date
        - Empty payload
        - Invalid (non existing) ID
        - Missing ID
"""


class TestPutBookingValid:

    def test_put_booking_all_new_values(self, api_client, auth_token, unique_booking):
        """
        Valid PUT request
        New values specified for ALL fields

        Expected result:
            - status code = 200
            - all fields have new values
        """
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
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

        response_json = response.json()

        flds = [
            'firstname',
            'lastname',
            'totalprice',
            'depositpaid',
            'additionalneeds'
        ]

        for fld in flds:
            assert response_json[fld] == updated_payload[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {updated_payload[fld]}.\n'
                f'Status code is {response.status_code}\n'
                f'{response_json}'
            )

        assert response_json['bookingdates']['checkin'] == updated_payload['bookingdates']['checkin'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkin']} != {updated_payload['bookingdates']['checkin']}.\n'
            f'Status code is {response.status_code}\n'
            f'{response_json}'
        )
        assert response_json['bookingdates']['checkout'] == updated_payload['bookingdates']['checkout'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkout']} != {updated_payload['bookingdates']['checkout']}.\n'
            f'Status code is {response.status_code}\n'
            f'{response_json}'
        )

    def test_put_booking_some_new_values(self, api_client, auth_token, unique_booking):
        """
        Valid PUT request
        New values specified for some fields, original values specified for other fields

        Expected result:
            - status code = 200
            - all fields have values specified in the request
        """
        target_id = unique_booking["id"]
        orig_data = unique_booking["data"]
        unique_suffix = str(int(time()))
        date_end = (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d")

        updated_payload = {
            "firstname": orig_data['firstname'],
            "lastname": f"TestLastname-{unique_suffix}",
            "totalprice": 350,
            "depositpaid": orig_data['depositpaid'],
            "bookingdates": {
                "checkin": orig_data['bookingdates']['checkin'],
                "checkout": date_end
            },
            "additionalneeds": orig_data['additionalneeds']
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

        response_json = response.json()

        flds = [
            'firstname',
            'lastname',
            'totalprice',
            'depositpaid',
            'additionalneeds'
        ]

        for fld in flds:
            assert response_json[fld] == updated_payload[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {updated_payload[fld]}.\n'
                f'Status code is {response.status_code}\n'
                f'{response_json}'
            )

        assert response_json['bookingdates']['checkin'] == updated_payload['bookingdates']['checkin'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkin']} != {updated_payload['bookingdates']['checkin']}.\n'
            f'Status code is {response.status_code}\n'
            f'{response_json}'
        )
        assert response_json['bookingdates']['checkout'] == updated_payload['bookingdates']['checkout'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkout']} != {updated_payload['bookingdates']['checkout']}.\n'
            f'Status code is {response.status_code}\n'
            f'{response_json}'
        )

    def test_put_booking_all_orig_values(self, api_client, auth_token, unique_booking):
        """
        Valid PUT request
        ALL fields have original values

        Expected result:
            - status code = 200
            - all fields have values specified in the request
        """
        target_id = unique_booking["id"]
        orig_data = unique_booking["data"]

        updated_payload = {
            "firstname": orig_data['firstname'],
            "lastname": orig_data['lastname'],
            "totalprice": orig_data['totalprice'],
            "depositpaid": orig_data['depositpaid'],
            "bookingdates": {
                "checkin": orig_data['bookingdates']['checkin'],
                "checkout": orig_data['bookingdates']['checkout']
            },
            "additionalneeds": orig_data['additionalneeds']
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

        response_json = response.json()

        flds = [
            'firstname',
            'lastname',
            'totalprice',
            'depositpaid',
            'additionalneeds'
        ]

        for fld in flds:
            assert response_json[fld] == updated_payload[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {updated_payload[fld]}.\n'
                f'Status code is {response.status_code}\n'
                f'{response_json}'
            )

        assert response_json['bookingdates']['checkin'] == updated_payload['bookingdates']['checkin'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkin']} != {updated_payload['bookingdates']['checkin']}.\n'
            f'Status code is {response.status_code}\n'
            f'{response_json}'
        )
        assert response_json['bookingdates']['checkout'] == updated_payload['bookingdates']['checkout'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkout']} != {updated_payload['bookingdates']['checkout']}.\n'
            f'Status code is {response.status_code}\n'
            f'{response_json}'
        )

    @pytest.mark.parametrize('missing_fld', [
        'firstname',
        'lastname',
        'totalprice',
        'depositpaid',
        'bookingdates'
    ])
    def test_put_booking_missing_field(self, api_client, auth_token, unique_booking, missing_fld):
        """
        Sending PUT request without one of the fields specified in the payload

        Expected result:
            - status code = 400/422
        """
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

        # removing the field
        updated_payload.pop(missing_fld)

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code in [400, 422], (
            f'Request unexpectedly accepted with the missing field {missing_fld}.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    def test_put_booking_send_same_payload_twice(self, api_client, auth_token, unique_booking):
        """
        Sending identical PUT request twice

        Expected result for the 1st request:
            - status code = 200
            - values specified in the payload updated
        Expected result for the 2nd request:
            - status code = 200
            - values are the same as after the 1st request
        """
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

        response_one = api_client.put(f"/booking/{target_id}",
                                      json=updated_payload, headers=headers)
        assert response_one.status_code == 200, f'Expecting status code 200, got {response_one.status_code}'

        response_two = api_client.put(f"/booking/{target_id}",
                                      json=updated_payload, headers=headers)
        assert response_two.status_code == 200, f'Expecting status code 200, got {response_two.status_code}'

        response_json = response_two.json()

        flds = [
            'firstname',
            'lastname',
            'totalprice',
            'depositpaid',
            'additionalneeds'
        ]

        for fld in flds:
            assert response_json[fld] == updated_payload[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {updated_payload[fld]}.\n'
                f'Status code is {response_json.status_code}\n'
                f'{response_json}'
            )

        assert response_json['bookingdates']['checkin'] == updated_payload['bookingdates']['checkin'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkin']} != {updated_payload['bookingdates']['checkin']}.\n'
            f'Status code is {response_json.status_code}\n'
            f'{response_json}'
        )
        assert response_json['bookingdates']['checkout'] == updated_payload['bookingdates']['checkout'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkout']} != {updated_payload['bookingdates']['checkout']}.\n'
            f'Status code is {response_json.status_code}\n'
            f'{response_json}'
        )

    @pytest.mark.parametrize('field_name', [
        'firstname',
        'lastname',
        'additionalneeds'
    ])
    def test_put_booking_long_str(self, api_client, auth_token, unique_booking, field_name):
        """
        Updating a string field to 1000 symbols

        The max len of string value is not documented, so this is only for test purposes

        Expected result:
            - status code = 200
            - field has new value
        """
        target_id = unique_booking["id"]
        unique_suffix = str(int(time()))
        orig_data = unique_booking["data"]

        updated_payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLastname-{unique_suffix}",
            "totalprice": orig_data['totalprice'],
            "depositpaid": orig_data['depositpaid'],
            "bookingdates": {
                "checkin": orig_data['bookingdates']['checkin'],
                "checkout": orig_data['bookingdates']['checkout']
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        updated_payload[field_name] = 'A' * 1000

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

        response_json = response.json()

        flds = [
            'firstname',
            'lastname',
            'totalprice',
            'depositpaid',
            'additionalneeds'
        ]

        for fld in flds:
            assert response_json[fld] == updated_payload[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {updated_payload[fld]}.\n'
                f'Status code is {response_json.status_code}\n'
                f'{response_json}'
            )

        assert response_json['bookingdates']['checkin'] == updated_payload['bookingdates']['checkin'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkin']} != {updated_payload['bookingdates']['checkin']}.\n'
            f'Status code is {response_json.status_code}\n'
            f'{response_json}'
        )
        assert response_json['bookingdates']['checkout'] == updated_payload['bookingdates']['checkout'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkout']} != {updated_payload['bookingdates']['checkout']}.\n'
            f'Status code is {response_json.status_code}\n'
            f'{response_json}'
        )


class TestPutBookingNegative:

    @pytest.mark.parametrize('null_fld', [
        'firstname',
        'lastname',
        'totalprice',
        'depositpaid',
        'bookingdates'
    ])
    def test_put_booking_null_value(self, api_client, auth_token, unique_booking, null_fld):
        """
        Sending PUT request with None value for one field

        Expected result:
            - status code = 400 or 422
        """
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

        updated_payload[null_fld] = None

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code in [400, 422], (
            f'Request unexpectedly accepted with the None value for {null_fld}.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    @pytest.mark.parametrize('empty_str', [
        'firstname',
        'lastname',
    ])
    @pytest.mark.xfail(reason='Empty string accepted as a new value')
    def test_put_booking_empty_str(self, api_client, auth_token, unique_booking, empty_str):
        """
        Sending PUT request with empty string value for string field

        Expected result:
            - status code = 400 or 422
        """
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

        updated_payload[empty_str] = ''

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code in [400, 422], (
            f'Request unexpectedly accepted with the empty field {empty_str}.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    @pytest.mark.parametrize('totalprice', [0, -1, 100.0])
    @pytest.mark.xfail(reason='no validation on totalprice field value')
    def test_put_booking_invalid_price(self, api_client, auth_token, unique_booking, totalprice):
        """
        Sending PUT request with invalid value for totalprice

        Expected result:
            - status code = 400 or 422
        """
        target_id = unique_booking["id"]
        unique_suffix = str(int(time()))
        date_start = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        date_end = (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d")

        updated_payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "lastname": f"TestLastname-{unique_suffix}",
            "totalprice": totalprice,
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
        assert response.status_code in [400, 422], (
            f'Request unexpectedly accepted with the total price == {totalprice}.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    @pytest.mark.xfail(reason='checkin > checkout is accepted')
    def test_put_booking_dates(self, api_client, auth_token, unique_booking):
        """
        Sending PUT request with checkin date > checkout date

        Expected result:
            - status code = 400 or 422
        """
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
                "checkin": date_end,
                "checkout": date_start
            },
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code in [400, 422], (
            f'Request unexpectedly accepted with checkin > checkout.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    def test_put_empty_payload(self, api_client, auth_token, unique_booking):
        """
        PUT request with empty payload

        Expected result:
            - status code = 400
        """
        target_id = unique_booking["id"]

        updated_payload = {
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 400, (
            f'Request unexpectedly accepted with empty payload.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

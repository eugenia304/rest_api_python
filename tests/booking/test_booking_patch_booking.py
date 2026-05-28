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
        - Only updated fields specified
        - All fields specified and have new values
        - Idempotency check 1: all fields specified and have original values
        - Idempotency check 2: send the same payload twice
        - Long string (>1000 chars)
    Negative:
        - Missing a field
        - NULL value for a field
        - Empty string as the string field value
        - Zero/negative price
        - Checkout date < Checkin date
        - ID not provided
        - Invalid ID provided
"""


class TestPatchBookingValid:

    @pytest.mark.xfail(reason='Date updates to 0NaN-aN-aN')
    def test_patch_booking_only_updated_flds(self, api_client, auth_token, unique_booking):
        """
        Valid PATCH request

        Only fields required updates specified in the payload

        Expected result:
            - status code = 200
            - fields specified in the payload have new values
            - fields not specified in the payload have original values
        """
        target_id = unique_booking["id"]
        orig_data = unique_booking["data"]
        unique_suffix = str(int(time()))
        date_end = (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d")

        updated_payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "totalprice": 350,
            "depositpaid": False,
            "bookingdates": {
                "checkout": date_end
            },
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.patch(f"/booking/{target_id}",
                                    json=updated_payload, headers=headers)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

        response_json = response.json()

        flds_upd = [
            'firstname',
            'totalprice',
            'depositpaid',
        ]

        flds_orig = [
            'lastname',
            'additionalneeds'
        ]

        for fld in flds_upd:
            assert response_json[fld] == updated_payload[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {updated_payload[fld]}.\n'
                f'Status code is {response.status_code}\n'
                f'{response_json}'
            )

        for fld in flds_orig:
            assert response_json[fld] == orig_data[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {orig_data[fld]}.\n'
                f'Status code is {response.status_code}\n'
                f'{response_json}'
            )

        assert response_json['bookingdates']['checkin'] == orig_data['bookingdates']['checkin'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkin']} != {orig_data['bookingdates']['checkin']}.\n'
            f'Status code is {response.status_code}\n'
            f'{response_json}'
        )
        assert response_json['bookingdates']['checkout'] == updated_payload['bookingdates']['checkout'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkout']} != {orig_data['bookingdates']['checkout']}.\n'
            f'Status code is {response.status_code}\n'
            f'{response_json}'
        )

    def test_patch_booking_all_new_values(self, api_client, auth_token, unique_booking):
        """
        Valid PATCH request, though it goes against the intended method application

        All fields specified in the payload with the new values

        Expected result:
            - status code = 200
            - fields specified in the payload have new values
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

        response = api_client.patch(f"/booking/{target_id}",
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

    @pytest.mark.xfail(reason='Date updates to 0NaN-aN-aN')
    def test_patch_booking_update_with_orig_values(self, api_client, auth_token, unique_booking):
        """
        Valid PATCH request, though it goes against the intended method application

        All fields specified in the payload with the original values

        Expected result:
            - status code = 200
            - fields specified in the payload have original values
        """
        target_id = unique_booking["id"]
        orig_data = unique_booking["data"]

        updated_payload = {
            "firstname": orig_data['firstname'],
            "totalprice": orig_data['totalprice'],
            "depositpaid": orig_data['depositpaid'],
            "bookingdates": {
                "checkin": orig_data['bookingdates']['checkin'],
            },
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.patch(f"/booking/{target_id}",
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
            assert response_json[fld] == orig_data[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {updated_payload[fld]}.\n'
                f'Status code is {response.status_code}\n'
                f'{response_json}'
            )

        assert response_json['bookingdates']['checkin'] == orig_data['bookingdates']['checkin'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkin']} != {orig_data['bookingdates']['checkin']}.\n'
            f'Status code is {response.status_code}\n'
            f'{response_json}'
        )
        assert response_json['bookingdates']['checkout'] == orig_data['bookingdates']['checkout'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkout']} != {orig_data['bookingdates']['checkout']}.\n'
            f'Status code is {response.status_code}\n'
            f'{response_json}'
        )

    @pytest.mark.xfail(reason='Date updates to 0NaN-aN-aN')
    def test_patch_booking_send_same_payload_twice(self, api_client, auth_token, unique_booking):
        """
        Valid PATCH request sent twice (idempotency check)

        Expected result for the 1st request:
            - status code = 200
            - fields specified in the payload have new values
            - fields not specified in the payload have original values

        Expected result for the 2nd request:
            - status code = 200
            - fields have the same values as after the 1st request
        """
        target_id = unique_booking["id"]
        orig_data = unique_booking["data"]
        unique_suffix = str(int(time()))
        date_end = (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d")

        updated_payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "totalprice": 350,
            "depositpaid": False,
            "bookingdates": {
                "checkout": date_end
            },
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response_one = api_client.patch(f"/booking/{target_id}",
                                        json=updated_payload, headers=headers)
        assert response_one.status_code == 200, f'Expecting status code 200, got {response_one.status_code}'

        response_two = api_client.patch(f"/booking/{target_id}",
                                        json=updated_payload, headers=headers)
        assert response_two.status_code == 200, f'Expecting status code 200, got {response_two.status_code}'

        response_json = response_two.json()

        flds_upd = [
            'firstname',
            'totalprice',
            'depositpaid',
        ]

        flds_orig = [
            'lastname',
            'additionalneeds'
        ]

        for fld in flds_upd:
            assert response_json[fld] == updated_payload[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {updated_payload[fld]}.\n'
                f'Status code is {response_json.status_code}\n'
                f'{response_json}'
            )
        for fld in flds_orig:
            assert response_json[fld] == orig_data[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {orig_data[fld]}.\n'
                f'Status code is {response_json.status_code}\n'
                f'{response_json}'
            )

        assert response_json['bookingdates']['checkin'] == orig_data['bookingdates']['checkin'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkin']} != {orig_data['bookingdates']['checkin']}.\n'
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
    def test_patch_booking_long_str(self, api_client, auth_token, unique_booking, field_name):
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
            "additionalneeds": f"Needs-{unique_suffix}"
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        updated_payload[field_name] = 'A' * 1000

        response = api_client.patch(f"/booking/{target_id}",
                                    json=updated_payload, headers=headers)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

        response_json = response.json()

        flds_upd = [
            'firstname',
            'lastname',
            'additionalneeds',
        ]

        flds_orig = [
            'totalprice',
            'depositpaid'
        ]

        for fld in flds_upd:
            assert response_json[fld] == updated_payload[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {updated_payload[fld]}.\n'
                f'Status code is {response_json.status_code}\n'
                f'{response_json}'
            )
        for fld in flds_orig:
            assert response_json[fld] == orig_data[fld], (
                f'Field values not updated or updated incorrectly:'
                f'{response_json[fld]} != {orig_data[fld]}.\n'
                f'Status code is {response_json.status_code}\n'
                f'{response_json}'
            )

        assert response_json['bookingdates']['checkin'] == orig_data['bookingdates']['checkin'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkin']} != {orig_data['bookingdates']['checkin']}.\n'
            f'Status code is {response_json.status_code}\n'
            f'{response_json}'
        )
        assert response_json['bookingdates']['checkout'] == orig_data['bookingdates']['checkout'], (
            f'Field values not updated or updated incorrectly:'
            f'{response_json['bookingdates']['checkout']} != {orig_data['bookingdates']['checkout']}.\n'
            f'Status code is {response_json.status_code}\n'
            f'{response_json}'
        )


class TestPatchBookingNegative:

    @pytest.mark.xfail(reason='Request accepted, no updates made to the original values')
    def test_patch_empty_payload(self, api_client, auth_token, unique_booking):
        """
        PATCH request with empty payload

        Expected result:
            - status code = 400
        """
        target_id = unique_booking["id"]

        updated_payload = {
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.patch(f"/booking/{target_id}",
                                    json=updated_payload, headers=headers)
        assert response.status_code == 400, (
            f'Request unexpectedly accepted with the empty payload.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    @pytest.mark.parametrize('null_fld', [
        'firstname',
        'lastname',
        'totalprice',
        'depositpaid',
        'bookingdates'
    ])
    def test_patch_booking_null_value(self, api_client, auth_token, unique_booking, null_fld):
        """
        Sending PATCH request with None value for one field

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

        response = api_client.patch(f"/booking/{target_id}",
                                    json=updated_payload, headers=headers)

        try:
            assert response.status_code == 400, f'Expecting status code 400, got {response.status_code}'
        except AssertionError as exc:
            if response.status_code == 500:
                pytest.xfail(
                    f'Known bug: status code == 500 instead of 400 for {null_fld}')
            elif response.status_code in [200, 201]:
                raise AssertionError(
                    f'Request unexpectedly accepted with the None value for {null_fld}.')

    @pytest.mark.parametrize('empty_str', [
        'firstname',
        'lastname',
    ])
    @pytest.mark.xfail(reason='Empty string accepted as a new value')
    def test_patch_booking_empty_str(self, api_client, auth_token, unique_booking, empty_str):
        """
        Sending PATCH request with empty string value for string field

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

        response = api_client.patch(f"/booking/{target_id}",
                                    json=updated_payload, headers=headers)
        assert response.status_code in [400, 422], (
            f'Request unexpectedly accepted with the empty field {empty_str}.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    @pytest.mark.parametrize('totalprice', [0, -1, 100.0])
    @pytest.mark.xfail(reason='no validation on totalprice field value')
    def test_patch_booking_invalid_price(self, api_client, auth_token, unique_booking, totalprice):
        """
        Sending PATCH request with invalid value for totalprice

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

        response = api_client.patch(f"/booking/{target_id}",
                                    json=updated_payload, headers=headers)
        assert response.status_code in [400, 422], (
            f'Request unexpectedly accepted with the total price == {totalprice}.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    @pytest.mark.xfail(reason='checkin > checkout is accepted')
    def test_patch_booking_dates(self, api_client, auth_token, unique_booking):
        """
        Sending PATCH request with checkin date > checkout date

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

        response = api_client.patch(f"/booking/{target_id}",
                                    json=updated_payload, headers=headers)
        assert response.status_code in [400, 422], (
            f'Request unexpectedly accepted with checkin > checkout.\n'
            f'Status code is {response.status_code}\n'
            f'{response.json()}'
        )

    def test_patch_booking_missing_id(self, api_client, auth_token):
        """
        PATCH request without ID provided


        Expected result:
            - status code = 404
        """

        unique_suffix = str(int(time()))
        date_end = (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d")

        updated_payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "totalprice": 350,
            "depositpaid": False,
            "bookingdates": {
                "checkout": date_end
            },
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.patch(f"/booking/",
                                    json=updated_payload, headers=headers)
        assert response.status_code == 404, f'Expecting status code 404, got {response.status_code}'

    @pytest.mark.xfail(reason='Expecting 404, got 405')
    def test_patch_booking_invalid_id(self, api_client, auth_token):
        """
        PATCH request with invalid (non existing) ID provided


        Expected result:
            - status code = 404
        """

        unique_suffix = str(int(time()))
        date_end = (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d")
        gen_id = str(int(time()))

        updated_payload = {
            "firstname": f"TestFirstname-{unique_suffix}",
            "totalprice": 350,
            "depositpaid": False,
            "bookingdates": {
                "checkout": date_end
            },
        }

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.patch(f"/booking/{gen_id}",
                                    json=updated_payload, headers=headers)
        assert response.status_code == 404, f'Expecting status code 404, got {response.status_code}'

import os

from datetime import datetime, timedelta
from time import time

"""
Test cases:
    - Valid Authorization: Basic header only
    - Both valid Authorization: Basic and Cookie: token headers
    - Valid Authorization: Basic header, invalid Cookie: token header
    - Invalid Authorization: Basic header, valid Cookie: token header
    - Invalid Authorization: Basic header, no Cookie: token header
    - Missing both headers
    - Invalid Cookie: token header, no Authorization: Basic header
"""


class TestAuthBasicPutBooking:

    def test_put_booking_auth_basic_valid(self, api_client, unique_booking):
        """
        Valid PUT request
        Authorization: Basic header is used
        Cookie: token header is omitted

        Expected result:
            - status code = 200
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
            'Authorization': os.getenv("BASIC_AUTH"),
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

    def test_put_booking_auth_valid_basic_and_token(self, api_client, auth_token, unique_booking):
        """
        Valid PUT request
        Authorization: Basic and Cookie: token headers are provided

        Expected result:
            - status code = 200
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
            'Authorization': os.getenv("BASIC_AUTH"),
            'Cookie': f'token={auth_token}',
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

    def test_put_booking_auth_valid_basic_invalid_token(self, api_client, unique_booking):
        """
        Valid PUT request
        Authorization: Basic and Cookie: token headers are provided
        Cookie: token contains invalid token

        Expected result:
            - status code = 200
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
            'Authorization': os.getenv("BASIC_AUTH"),
            'Cookie': 'token=123456',
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

    def test_put_booking_auth_invalid_basic_valid_token(self, api_client, auth_token, unique_booking):
        """
        Valid PUT request
        Authorization: Basic and Cookie: token headers are provided
        Cookie: token contains invalid token

        Expected result:
            - status code = 200
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
            'Authorization': 'Basic badCredentialsString123',
            'Cookie': f'token={auth_token}',
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

    def test_put_booking_auth_invalid_basic_no_token(self, api_client, auth_token, unique_booking):
        """
        Valid PUT request
        Authorization: Basic header contains invalid value
        Cookie: token not provided

        Expected result:
            - status code = 403
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
            'Authorization': 'Basic badCredentialsString123',
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 403, f'Expecting status code 403, got {response.status_code}'

    def test_put_booking_missing_token_and_basic(self, api_client, unique_booking):
        """
        Valid PUT request with missing auth token

        Expected result:
            - status code = 403
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

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload)
        assert response.status_code == 403, f'Expecting status code 200, got {response.status_code}'

    def test_put_booking_invalid_token_no_basic(self, api_client, unique_booking):
        """
        Valid PUT request with invalid auth token

        Expected result:
            - status code = 403
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
            'Cookie': 'token=123456'
        }

        response = api_client.put(f"/booking/{target_id}",
                                  json=updated_payload, headers=headers)
        assert response.status_code == 403, f'Expecting status code 200, got {response.status_code}'

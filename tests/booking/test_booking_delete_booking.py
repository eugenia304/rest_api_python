import pytest

from time import time


"""
Returns status code 201

Test cases:
    Valid request:
        - Delete booking specifying valid ID
    Authorization:
        - Missing token
        - Invalid token
    Negative:
        - Booking ID invalid (non existing)
        - Booking ID not provided
        - Two identical requests sent in a row
"""


class TestDeleteBooking:

    def test_delete_booking_valid(self, api_client, auth_token, unique_booking):
        """
        Valid DELETE request

        Expected result:
            - status code = 201
            - entry deleted (status code 404 for GET by ID)
        """
        target_id = unique_booking["id"]

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.delete(f"/booking/{target_id}", headers=headers)
        assert response.status_code == 201, f'Expecting status code 201, got {response.status_code}'

        # sending GET to verify that booking with provided ID does not exist
        response_get = api_client.get(f'/booking/{target_id}', headers=headers)
        assert response_get.status_code == 404, f'Expecting status code 404, got {response_get.status_code}'


class TestDeleteBookingNegative:

    @pytest.mark.xfail(reason='Expecting 404, got 405')
    def test_delete_booking_invalid_id(self, api_client, auth_token):
        """
        DELETE request with invalid (non existing) ID

        Expected result:
            - status code = 404
        """
        gen_id = str(int(time()))

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.delete(f"/booking/{gen_id}", headers=headers)
        assert response.status_code == 404, f'Expecting status code 404, got {response.status_code}'

    def test_delete_booking_id_not_provided(self, api_client, auth_token):
        """
        DELETE request with missing ID

        Expected result:
            - status code = 404
        """
        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.delete(f"/booking/", headers=headers)
        assert response.status_code == 404, f'Expecting status code 404, got {response.status_code}'

    @pytest.mark.xfail(reason='Expecting 404, got 405')
    def test_delete_booking_two_requests(self, api_client, auth_token, unique_booking):
        """
        Sending 2 identical DELETE requests in a row

        Expected result for the 1st request:
            - status code = 201
            - entry deleted (status code 404 for GET by ID)
        Expected result for the 2nd request:
            - status code = 404
        """
        target_id = unique_booking["id"]

        headers = {
            'Cookie': f'token={auth_token}',
        }

        response = api_client.delete(f"/booking/{target_id}", headers=headers)
        assert response.status_code == 201, f'Expecting status code 201, got {response.status_code}'

        # sending GET to verify that booking with provided ID does not exist
        response_get = api_client.get(f'/booking/{target_id}', headers=headers)
        assert response_get.status_code == 404, f'Expecting status code 404, got {response.status_code}'

        response = api_client.delete(f"/booking/{target_id}", headers=headers)
        assert response.status_code == 404, f'Expecting status code 404, got {response.status_code}'

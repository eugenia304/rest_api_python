import os
import pytest

"""
Test cases:
    - Valid Authorization: Cookie header only
    - Valid Authorization: Basic header only
    - Both valid Authorization: Basic and Cookie: token headers
    - Valid Authorization: Basic header, invalid Cookie: token header
    - Invalid Authorization: Basic header, valid Cookie: token header
    - Invalid Authorization: Basic header, no Cookie: token header
    - Missing both headers
    - Invalid Cookie: token header, no Authorization: Basic header
"""


@pytest.mark.skip_cleanup
class TestDeleteBookingAuth:

    def test_delete_booking_auth_cookie_valid(self, api_client, auth_token, unique_booking):
        """
        Valid DELETE request
        Authorization: Cookie header is used

        Expected result:
            - status code = 201
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

    def test_delete_booking_auth_basic_valid(self, api_client, unique_booking):
        """
        Valid DELETE request
        Authorization: Basic header is used
        Cookie: token header is omitted

        Expected result:
            - status code = 201
        """
        target_id = unique_booking["id"]

        headers = {
            'Authorization': os.getenv("BASIC_AUTH"),
        }

        response = api_client.delete(f"/booking/{target_id}", headers=headers)
        assert response.status_code == 201, f'Expecting status code 201, got {response.status_code}'

        # sending GET to verify that booking with provided ID does not exist
        response_get = api_client.get(f'/booking/{target_id}', headers=headers)
        assert response_get.status_code == 404, f'Expecting status code 404, got {response_get.status_code}'

    def test_delete_booking_auth_valid_basic_and_token(self, api_client, auth_token, unique_booking):
        """
        Valid DELETE request
        Authorization: Basic and Cookie: token headers are provided

        Expected result:
            - status code = 201
        """
        target_id = unique_booking["id"]

        headers = {
            'Authorization': os.getenv("BASIC_AUTH"),
            'Cookie': f'token={auth_token}',
        }

        response = api_client.delete(f"/booking/{target_id}", headers=headers)
        assert response.status_code == 201, f'Expecting status code 201, got {response.status_code}'

        # sending GET to verify that booking with provided ID does not exist
        response_get = api_client.get(f'/booking/{target_id}', headers=headers)
        assert response_get.status_code == 404, f'Expecting status code 404, got {response_get.status_code}'

    def test_delete_booking_auth_valid_basic_invalid_token(self, api_client, unique_booking):
        """
        Valid PUT request
        Authorization: Basic and Cookie: token headers are provided
        Cookie: token contains invalid token

        Expected result:
            - status code = 201
        """
        target_id = unique_booking["id"]

        headers = {
            'Authorization': os.getenv("BASIC_AUTH"),
            'Cookie': 'token=123456',
        }

        response = api_client.delete(f"/booking/{target_id}", headers=headers)
        assert response.status_code == 201, f'Expecting status code 201, got {response.status_code}'

        # sending GET to verify that booking with provided ID does not exist
        response_get = api_client.get(f'/booking/{target_id}', headers=headers)
        assert response_get.status_code == 404, f'Expecting status code 404, got {response_get.status_code}'

    def test_delete_booking_auth_invalid_basic_valid_token(self, api_client, auth_token, unique_booking):
        """
        Valid DELETE request
        Authorization: Basic and Cookie: token headers are provided
        Cookie: token contains invalid token

        Expected result:
            - status code = 201
        """
        target_id = unique_booking["id"]

        headers = {
            'Authorization': 'Basic badCredentialsString123',
            'Cookie': f'token={auth_token}',
        }

        response = api_client.delete(f"/booking/{target_id}", headers=headers)
        assert response.status_code == 201, f'Expecting status code 201, got {response.status_code}'

        # sending GET to verify that booking with provided ID does not exist
        response_get = api_client.get(f'/booking/{target_id}', headers=headers)
        assert response_get.status_code == 404, f'Expecting status code 404, got {response_get.status_code}'

    def test_delete_booking_auth_invalid_basic_no_token(self, api_client, unique_booking):
        """
        Valid DELETE request
        Authorization: Basic header contains invalid value
        Cookie: token not provided

        Expected result:
            - status code = 403
        """
        target_id = unique_booking["id"]

        headers = {
            'Authorization': 'Basic badCredentialsString123',
        }

        response = api_client.delete(f"/booking/{target_id}", headers=headers)
        assert response.status_code == 403, f'Expecting status code 403, got {response.status_code}'

    def test_delete_booking_missing_token_and_basic(self, api_client, unique_booking):
        """
        Valid DELETE request with missing auth token

        Expected result:
            - status code = 403
        """
        target_id = unique_booking["id"]

        response = api_client.delete(f"/booking/{target_id}")
        assert response.status_code == 403, f'Expecting status code 403, got {response.status_code}'

    def test_delete_booking_invalid_token_no_basic(self, api_client, unique_booking):
        """
        Valid DELETE request with invalid auth token

        Expected result:
            - status code = 403
        """
        target_id = unique_booking["id"]

        headers = {
            'Cookie': 'token=123456'
        }

        response = api_client.delete(f"/booking/{target_id}", headers=headers)
        assert response.status_code == 403, f'Expecting status code 403, got {response.status_code}'

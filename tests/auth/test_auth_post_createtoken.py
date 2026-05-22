import pytest
import os


"""
Test cases:
    Valid:
        - Create new token with valid username/password provided
    Payload validations:
        - Create new token with invalid username provided
        - Create new token with invalid password provided
        - Create new token without username field
        - Create new token without password field
        - Create new token with empty payload
"""


class TestAuthValid:

    def test_auth_success(self, api_client):
        """
        POST auth with correct credentials specified

        Expected result:
            - status code = 200
            - token generated
        """
        payload = {
            'username': os.getenv("USERNAME"),
            'password': os.getenv("PASSWORD")
        }

        response = api_client.post(
            "/auth",
            json=payload
        )
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'
        assert response.json()['token'] is not None, 'Token not generated'


class TestAuthPayload:

    @pytest.mark.xfail(reason='Expected 401, got 200 with text Bad Credentials')
    @pytest.mark.parametrize("user", ['user', 'Admin', ' ', ''])
    def test_auth_invalid_username(self, api_client, user):
        """
        POST auth with incorrect credentials (username) specified

        Expected result:
            - status code = 401
            - token not generated
        """
        payload = {
            'username': user,
            'password': os.getenv("PASSWORD")
        }

        response = api_client.post(
            "/auth",
            json=payload
        )

        assert response.status_code == 401, f'Expecting status code 401, got {response.status_code}'

    @pytest.mark.xfail(reason='Expected 401, got 200 with text Bad Credentials')
    @pytest.mark.parametrize("password", ['password', ' password123', 'password123 ', ' ', ''])
    def test_auth_invalid_password(self, api_client, password):
        """
        POST auth with incorrect credentials (password) specified

        Expected result:
            - status code = 401
            - token not generated
        """
        payload = {
            'username': os.getenv("USERNAME"),
            'password': password
        }

        response = api_client.post(
            "/auth",
            json=payload
        )

        assert response.status_code == 401, f'Expecting status code 401, got {response.status_code}'

    def test_auth_req_missing_username(self, api_client):
        """
        POST auth with missing credentials (username)

        Expected result:
            - status code = 400
            - token not generated
        """
        payload = {
            'password': os.getenv("PASSWORD")
        }

        response = api_client.post(
            "/auth",
            data=payload
        )

        assert response.status_code == 400, f'Expecting status code 400, got {response.status_code}'

    def test_auth_req_missing_password(self, api_client):
        """
        POST auth with missing credentials (password)

        Expected result:
            - status code = 400
            - token not generated
        """
        payload = {
            'username': os.getenv("USERNAME")
        }

        response = api_client.post(
            "/auth",
            data=payload
        )

        assert response.status_code == 400, f'Expecting status code 400, got {response.status_code}'

    @pytest.mark.xfail(reason='200 - Bad credentials')
    def test_auth_req_empty_payload(self, api_client):
        """
        POST auth with empty payload

        Expected result:
            - status code = 400
            - token not generated
        """
        payload = {
        }

        response = api_client.post(
            "/auth",
            data=payload
        )
        assert response.status_code == 400, f'Expecting status code 400, got {response.status_code}'


class TestAuthMethods:

    @pytest.mark.parametrize("method, expected_status", [
        ("get", 405),
        ("put", 405),
        ("patch", 405),
        ("delete", 405),
    ])
    @pytest.mark.xfail(reason='404 (Not Found) instead of 405 (Method Not Allowed)')
    def test_auth_methods(self, api_client, method, expected_status):
        """
        Different methods for endpoint (only post is supported)

        Expected result:
            - status code = 405
        """

        request_func = getattr(api_client, method)

        response = request_func(
            "/auth",
        )

        assert response.status_code == expected_status, f'Expecting status code {expected_status}, got {response.status_code}'

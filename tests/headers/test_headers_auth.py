import os
import pytest

from dicttoxml import dicttoxml

"""
Test cases:
    - Content-Type: value different from the actual data provided
    - Content-Type: value different from application/json (correct format provided)
    - Accept: received data is in correct format
    - Content-Type: field is missing
    - Content-Type: specified as content-type
    - Content-Type: specified twice with different values
    - Accept: specified twice with different values
    - Checking GET/PUT/PATCH/DELETE methods are not allowed
"""


class TestAuthHeaders:

    payload_json = {
        'username': os.getenv("USERNAME"),
        'password': os.getenv("PASSWORD")
    }

    payload_xml = dicttoxml(payload_json)

    @pytest.mark.parametrize("contenttype, payload, expected_status, expected_body", [
        ("text/plain", payload_json, 200, "Bad credentials"),
        ("text/plain", payload_xml, 200, "Bad credentials"),
        ("application/xml", payload_json, 400, "Bad Request"),
        ("application/json", payload_xml, 400, "Bad Request"),
        ("", payload_json, 200, "Bad credentials"),
        ("", payload_xml, 200, "Bad credentials"),
        ("text/plain", 'username: admin, password: password123', 200, "Bad credentials"),
        ("application/xml", payload_xml, 200, "Bad credentials"),
    ])
    def test_post_auth_contenttype(self, api_client, contenttype, payload,
                                   expected_status, expected_body):
        """
        Different Content-Type values

        Expected result:
            - status code = 200, reason = Bad Credentials, or
            - status code = 400 - Bad Request
        """
        headers = {
            'Content-Type': contenttype
        }

        response = api_client.post('/auth', headers=headers, data=payload)

        assert response.status_code == expected_status, f'Expecting status code {expected_status}, got {response.status_code}'
        assert expected_body in response.text, f'Expecting reason {expected_body}, got {response.text}'

    @pytest.mark.parametrize("accept_format, expected_response_type", [
        ("application/json", "application/json"),
        pytest.param(
            "application/xml", "application/xml",
            marks=pytest.mark.xfail(
                reason="Restful-Booker ignores Accept headers")
        )
    ])
    def test_post_auth_accept(self, api_client, accept_format, expected_response_type):
        """
        Checking that data in response is in format specified in the Accept header
        """
        headers = {
            'Accept': accept_format,
        }

        response = api_client.post(
            '/auth', headers=headers, json=self.payload_json)

        assert expected_response_type in response.headers[
            "Content-Type"], f'Expecting response type {expected_response_type}, got {response.headers["Content-Type"]}'

    @pytest.mark.xfail(reason='Missing Content-Type header in request is ignored')
    def test_auth_req_headers_contenttype_missing(self, api_client):
        """
        Sending request without Content-Type header
        """

        headers = {
            'Content-Type': None,
        }

        response = api_client.post(
            '/auth', headers=headers, json=self.payload_json)

        assert response.status_code in [
            400, 415], f'Expecting status code 400/415, got {response.status_code}'

    def test_auth_req_headers_contenttype_lowercase(self, api_client):
        """
        Sending request with content-type header instead of Content-Type
        """

        headers = {
            'content-type': 'application/json'
        }

        response = api_client.post(
            '/auth', headers=headers, json=self.payload_json)

        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'
        assert response.json()['token'] is not None, 'Token not generated'

    def test_auth_req_headers_contenttype_dupl(self, api_client):
        """
        Sending request with Content-Type header specified twice
        """
        headers = {
            'Content-Type': 'application/json',
            'Content-Type': 'application/xml'
        }

        response = api_client.post(
            '/auth', headers=headers, json=self.payload_json)

        assert response.status_code in [
            400, 415], f'Expecting status code 400/415, got {response.status_code}'

    def test_auth_req_headers_accept_dupl(self, api_client):
        """
        Sending request with Accept header specified twice
        """

        headers = {
            'Accept': 'application/xml',
            'Accept': 'application/json',
        }

        response = api_client.post(
            '/auth', headers=headers, json=self.payload_json)

        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'
        assert response.json()['token'] is not None, 'Token not generated'

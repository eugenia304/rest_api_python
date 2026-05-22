import pytest
import requests
import allure
import json

from datetime import datetime, timedelta
from dotenv import load_dotenv
from time import time

from schemas.auth import AuthRequest


BASE_URL = "https://restful-booker.herokuapp.com"
load_dotenv()


class APIClient:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

        # Default headers
        # If another value is set inside the test, it will override the below value
        # To remove the header set '<header>': None
        # If any other headers specified inside the test, they will be added to the list
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _send_request(self, method: str, endpoint: str, **kwargs):
        """Internal helper to forward requests, apply URLs, and attach data to Allure."""
        url = f"{self.base_url}{endpoint}"

        # Catch explicit method overrides if passed locally
        response = self.session.request(method, url, **kwargs)

        # Step-logging inside Allure Reports
        with allure.step(f"HTTP {method} -> {endpoint}"):
            allure.attach(
                body=json.dumps(dict(response.request.headers), indent=2),
                name="Request Headers",
                attachment_type=allure.attachment_type.JSON
            )
            if kwargs.get("json"):
                allure.attach(
                    body=json.dumps(kwargs.get("json"), indent=2),
                    name="Request Body",
                    attachment_type=allure.attachment_type.JSON
                )
            allure.attach(
                body=f"Status Code: {response.status_code}\n\n{response.text}",
                name="Response Context",
                attachment_type=allure.attachment_type.TEXT
            )

        return response

    def get(self, endpoint: str, **kwargs):
        return self._send_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, data=None, json=None, **kwargs):
        return self._send_request("POST", endpoint, json=json, data=data, **kwargs)

    def put(self, endpoint: str, json=None, **kwargs):
        return self._send_request("PUT", endpoint, json=json, **kwargs)

    def patch(self, endpoint: str, json=None, **kwargs):
        return self._send_request("PATCH", endpoint, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._send_request("DELETE", endpoint, **kwargs)


@pytest.fixture(scope="session")
def api_client():
    """
    Shared API client for all tests
    """
    return APIClient(BASE_URL)


@pytest.fixture(scope='session', autouse=True)
def auth_token(api_client):
    """
    Returns the generated token
    """
    payload = AuthRequest(
        username="admin",
        password="password123"
    )
    headers = {
        'accept': '*/*',
        'Referer': '',
        'Content-Type': 'application/json'
    }

    response = api_client.post(
        "/auth",
        headers=headers,
        json=payload.model_dump()
    )
    token = response.json().get('token')

    return token


@pytest.fixture
def unique_booking(api_client, auth_token):
    # Timestamp used to guarantee a unique name
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

    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}
    auth_headers = {'Cookie': f'token = {auth_token}',
                    'Authorization': 'Basic'}

    response = api_client.post("/booking", json=payload, headers=headers)
    assert response.status_code == 200

    booking_data = response.json()
    booking_id = booking_data["bookingid"]

    # Provide the ID and the unique payload to the test
    yield {"id": booking_id, "data": booking_data["booking"]}

    # Deleting the booking after the test
    api_client.delete(f"/booking/{booking_id}", headers=auth_headers)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Automated hook that runs on test execution phases.
    Intercepts failures and prints full HTTP Request/Response logs.
    """
    # Let the test execution phase complete
    outcome = yield
    report = outcome.get_result()

    # Only intercept actual call execution failures (ignore setup/teardown)
    if report.when == "call" and report.failed:
        # Look for the api_client fixture or request library hooks inside the test
        if "api_client" in item.funcargs:
            print("\n" + "="*60)
            print("🚨 AUTOMATED API NETWORK FAILURE TRACE 🚨")
            print("="*60)

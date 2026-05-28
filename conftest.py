import pytest
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv
from time import time

from src.client import APIClient


load_dotenv()


@pytest.fixture(scope="session")
def api_client(pytestconfig):
    """
    Shared API client for all tests
    """
    return APIClient(pytestconfig.getoption('base_url'))


@pytest.fixture(scope='session', autouse=True)
def auth_token(api_client):
    """
    Returns the generated token
    """
    payload = {
        'username': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD')
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = api_client.post(
        "/auth",
        headers=headers,
        json=payload
    )
    token = response.json().get('token')

    return token


@pytest.fixture
def unique_booking(request, api_client, auth_token):
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

    if request.node.get_closest_marker("skip_cleanup"):
        return  # Exit without deleting a booking

    try:
        # Deleting the booking after the test
        api_client.delete(f"/booking/{booking_id}", headers=auth_headers)
    except Exception as e:
        print(f"\nBooking was not deleted: {e}")


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
            print("FAILURE")
            print("="*60)

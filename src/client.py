import requests
import allure
import json


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

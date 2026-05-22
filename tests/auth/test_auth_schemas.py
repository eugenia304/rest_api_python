from src.schemas.auth import AuthSuccessResponse, AuthErrorResponse


class TestAuthSchemas:

    def test_schema_post_auth_valid(self, api_client):
        """
        Auth response schema validation for valid request
        """
        payload = {
            'username': "admin",
            'password': "password123"
        }

        response = api_client.post(
            "/auth",
            json=payload
        )

        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

        response_json = response.json()
        assert isinstance(
            response_json, dict), f"Expected dict, got {type(response_json)}"

        validated_response = AuthSuccessResponse.model_validate(
            response_json)
        assert len(validated_response.token) > 0, 'Token not generated'

    def test_schema_post_auth_invalid(self, api_client):
        """
        Auth response schema validation for invalid request
        """
        payload = {
            'username': "admin",
            'password': "invalid_password"
        }

        response = api_client.post(
            "/auth",
            json=payload
        )

        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

        response_json = response.json()
        assert isinstance(
            response_json, dict), f"Expected dict, got {type(response_json)}"

        validated_response = AuthErrorResponse.model_validate(
            response_json)
        assert validated_response.reason == "Bad credentials", f'Unexpected reason: {validated_response.reason}'

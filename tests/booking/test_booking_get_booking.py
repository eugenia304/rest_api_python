import pytest

from time import time


"""
Booking details have the following format:
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
    - GET booking ids 
    - GET booking details by id
    - GET booking ids by single field (firstname, lastname, additionalneeds, checkin, checkout)
    - GET booking details by non existing id
    - GET booking ids by non existing field
    - GET booking ids by non existing field value (firstname, lastname, additionalneeds, checkin, checkout)
"""


class TestGetBooking:

    def test_get_booking_ids(self, api_client):
        """
        GET all booking IDs

        Expected result:
            - status code = 200
        """

        response = api_client.get(
            '/booking')

        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

    def test_get_booking_details_by_id(self, api_client, unique_booking):
        """
        GET booking details by booking ID

        Expected result:
            - status code = 200
        """
        target_id = unique_booking["id"]
        expected_data = unique_booking["data"]

        response = api_client.get(
            f'/booking/{target_id}')

        response_json = response.json()
        assert isinstance(
            response_json, dict), f"Expected a single JSON object dictionary, got {type(response_json)}"
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

        # Validating response against the actual sent data
        flds = [
            'firstname',
            'lastname',
            'totalprice',
            'depositpaid',
            'additionalneeds'
        ]

        for fld in flds:
            actual_value = response_json[fld]
            expected_value = expected_data[fld]
            assert actual_value == expected_value, (
                f"Mismatch found in field '{fld}'"
                f"Expected: {expected_value}, Got: {actual_value}"
            )

    @pytest.mark.parametrize("fld", [
        'firstname',
        'lastname',
        pytest.param(
            "additionalneeds",
            marks=pytest.mark.xfail(
                reason="filtering by additionalneeds not working as expected")
        ),
        pytest.param(
            "checkin",
            marks=pytest.mark.xfail(
                reason="filtering by checkin not working as expected")
        ),
        'checkout',
    ])
    def test_get_booking_ids_by_single_field(self, api_client, unique_booking, fld):
        """
        GET booking IDs by field=value filter

        Expected result:
            - status code = 200
            - a list of booking ids with field = value
        """

        target_id = unique_booking["id"]
        data = unique_booking["data"]

        if fld in ['checkin', 'checkout']:
            params = {fld: data['bookingdates'][fld]}
        else:
            params = {fld: data[fld]}

        response = api_client.get(
            '/booking', params=params)
        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'

        response_items = response.json()

        # Get all IDs
        returned_ids = [item['bookingid'] for item in response_items]

        # Checking that the booking is in the filtered list
        assert target_id in returned_ids, f"Booking ID {target_id} not found by {fld}"

        # All the fields except for checkin/checkout have unique values
        if fld not in ['checkin', 'checkout']:
            assert len(
                response_items) == 1, f'Expecting 1 item, got {len(response_items)} items'


class TestGetBookingNegative:

    def test_get_booking_details_by_non_existent_id(self, api_client):
        """
        GET booking by invalid (non existing) ID

        Expected result:
            - status code = 400
        """
        gen_id = str(int(time()))

        response = api_client.get(
            f'/booking/{gen_id}')

        assert response.status_code == 404, f'Expecting status code 404, got {response.status_code}'

    @pytest.mark.xfail(reason='non existing field is ignored')
    def test_get_booking_ids_by_non_existing_fld(self, api_client):
        """
        GET booking by invalid (non existing) field

        Expected result:
            - status code = 400
        """
        params = {'room': 1}

        response = api_client.get(
            f'/booking', params=params)
        assert response.status_code == 400, f'Expecting status code 400, got {response.status_code}'

    @pytest.mark.parametrize("fld", [
        'firstname',
        'lastname',
        pytest.param(
            "additionalneeds",
            marks=pytest.mark.xfail(
                reason="filtering by non existing value for additionalneeds returns all IDs")
        )
    ])
    def test_get_booking_ids_by_non_existent_fld_value(self, api_client, fld):
        """
        GET booking by invalid (non existing) value for existing field

        Expected result:
            - status code = 200
            - empty response body
        """
        gen_val = str(int(time()))
        params = {fld: gen_val}

        response = api_client.get(
            f'/booking', params=params)

        assert response.status_code == 200, f'Expecting status code 200, got {response.status_code}'
        assert len(response.json()
                   ) == 0, f'{len(response.json())} unexpected items returned'

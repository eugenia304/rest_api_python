## Table of Contents

[Project Structure](#project-structure)\
[Reporting](#reporting)\
[Test Cases](#test-cases)

## Project Structure

The project has the following structure:

- conftest.py
- pytest.ini
- requirements.txt
- src
  - __init__.py
  - client.py
  - schemas
    - __init__.py
    - auth.py
    - booking.py
- tests
  - auth
  - booking
  - headers

 `src` directory stores the Pydantic schema files (`schemas/`) and the API client class (`client.py`).\
 `tests` directory stores all the test files in respective sub directories (`auth`, `booking`, `headers`).

 ## Reporting

 Allure reporting is used in the project. To see the report run\
 `allure serve allure-results`\
 after the test execution.

 ## Test Cases

 ### Auth
**Schema Validation**
 - Response schema for valid request
 - Response schema for invalid request

**DELETE Booking**
- Valid Authorization: Basic header only
- Both valid Authorization: Basic and Cookie: token headers
- Valid Authorization: Basic header, invalid Cookie: token header
- Invalid Authorization: Basic header, valid Cookie: token header
- Invalid Authorization: Basic header, no Cookie: token header
- Missing both headers
- Invalid Cookie: token header, no Authorization: Basic 

**PATCH Booking**
- Valid Authorization: Basic header only
- Both valid Authorization: Basic and Cookie: token headers
- Valid Authorization: Basic header, invalid Cookie: token header
- Invalid Authorization: Basic header, valid Cookie: token header
- Invalid Authorization: Basic header, no Cookie: token header
- Missing both headers
- Invalid Cookie: token header, no Authorization: Basic header

**PUT Booking**
- Valid Authorization: Basic header only
- Both valid Authorization: Basic and Cookie: token headers
- Valid Authorization: Basic header, invalid Cookie: token header
- Invalid Authorization: Basic header, valid Cookie: token header
- Invalid Authorization: Basic header, no Cookie: token header
- Missing both headers
- Invalid Cookie: token header, no Authorization: Basic header

**POST Create Token**
- Create new token with valid username/password provided
- Create new token with invalid username provided
- Create new token with invalid password provided
- Create new token without username field
- Create new token without password field
- Create new token with empty payload

### Booking

**POST (create) Booking**
- Create booking by providing valid values for all fields
- Long string (>1000 chars)
- Idempotency check: send the same payload twice to verify that they get different booking ids

**DELETE Booking**
- Delete booking specifying valid ID
- Booking ID invalid (non existing)
- Booking ID not provided
- Two identical requests sent in a row

**GET Booking**
- GET booking ids 
- GET booking details by id
- GET booking ids by single field (firstname, lastname, additionalneeds, checkin, checkout)
- GET booking details by non existing id
- GET booking ids by non existing field
- GET booking ids by non existing field value (firstname, lastname, additionalneeds, checkin, checkout)

**PATCH Booking**
- Valid request:
  - Only updated fields specified
  - All fields specified and have new values
  - Idempotency check 1: all fields specified and have original values
  - Idempotency check 2: send the same payload twice
  - Long string (>1000 chars)
- Negative:
  - Missing a field
  - NULL value for a field
  - Empty string as the string field value
  - Zero/negative price
  - Checkout date < Checkin date
  - ID not provided
  - Invalid ID provided

**PUT Booking**
- Valid request:
  - All fields specified and have new values
  - All fields specified but some have original values
  - All fields specified and have original values
  - One of the fields not specified in the request
  - Idempotency check: send the same payload twice
  - Long string (>1000 chars)
- Negative:
  - NULL value for a field
  - Empty string as the string field value
  - Zero/negative price
  - Checkout date < Checkin date
  - Empty payload
  - Invalid (non existing) ID
  - Missing ID

**Schema Validation**
- GET /booking
- GET /booking/:id
- POST /booking
- PUT /booking/:id
- PATCH /booking/:id
- DELETE /booking/:id

### Headers
For `auth/` only
- Content-Type: value different from the actual data provided
- Content-Type: value different from application/json (correct format provided)
- Accept: checking that received data is in correct format
- Content-Type: field is missing
- Content-Type: specified as content-type
- Content-Type: specified twice with different values
- Accept: specified twice with different values
- Checking GET/PUT/PATCH/DELETE methods are not allowed

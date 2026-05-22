from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


# -------------------------
# AUTH REQUEST
# -------------------------

class AuthRequest(BaseModel):
    """
    Request to create new token
    min_length set to 0 to test an empty string being sent
    """
    model_config = ConfigDict(extra="allow")

    username: str = Field(..., min_length=0)
    password: str = Field(..., min_length=0)

# -------------------------
# AUTH SUCCESS RESPONSE
# -------------------------


class AuthSuccessResponse(BaseModel):
    """
    Response to correct request
    """
    model_config = ConfigDict(extra="forbid")

    token: str = Field(..., min_length=1)


# -------------------------
# AUTH FAILURE RESPONSE
# -------------------------

class AuthErrorResponse(BaseModel):
    """
    Response to incorrect request (incorrect or missing credentials)
    { "reason": "Bad credentials" }
    """
    model_config = ConfigDict(extra="forbid")

    reason: str

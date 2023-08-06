

REQUEST_BODY_JSON = """
{
    "username": "string",
    "password": "string"
}
"""


RESPONSE_200_JSON = """
{
    "user_id": 1,
    "access_token": "string",
    "refresh_token": "string",
    "expires_in": "2099-12-31 00:00:00"
}
"""

RESPONSE_401_JSON = """
{
    "msg": "string",
    "res_status": "INVALID_USERNAME"
}
"""


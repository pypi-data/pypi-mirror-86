

REQUEST_BODY_JSON = """
{
    "item_details": [
        {
            "item_id": 1,
            "brand_details": {
                "brand_id": 1
            },
            "ordered_quantity": 1
        }
    ]
}
"""


RESPONSE_400_JSON = """
{
    "msg": "string",
    "res_status": "INVALID_ITEM"
}
"""

RESPONSE_404_JSON = """
{
    "msg": "string",
    "res_status": "INVALID_FORM"
}
"""


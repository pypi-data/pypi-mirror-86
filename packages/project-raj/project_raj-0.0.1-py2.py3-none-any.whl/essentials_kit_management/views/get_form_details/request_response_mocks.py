


RESPONSE_200_JSON = """
{
    "form_name": "string",
    "form_description": "string",
    "sections": [
        {
            "section_id": 1,
            "section_name": "string",
            "section_description": "string",
            "item_details": [
                {
                    "item_id": 1,
                    "item_name": "string",
                    "item_description": "string",
                    "item_brands": [
                        {
                            "brand_id": 1,
                            "brand_name": "string",
                            "item_price": 1,
                            "min_quantity": 1,
                            "max_quantity": 1
                        }
                    ],
                    "order_details": {
                        "brand_id": 1,
                        "item_price": 1.1,
                        "ordered_quantity": 1,
                        "delivered_quantity": 1,
                        "is_out_of_stock": true
                    }
                }
            ]
        }
    ],
    "total_cost": 1.1,
    "total_items": 1
}
"""


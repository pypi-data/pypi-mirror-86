# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase02GetFormDetailsAPITestCase::test_case status'] = 200

snapshots['TestCase02GetFormDetailsAPITestCase::test_case body'] = {
    'close_date': '2020-06-26 17:23:01',
    'form_description': 'This is the Form of Form 10',
    'form_id': 10,
    'form_name': 'Form 10',
    'sections': [
        {
            'item_details': [
                {
                    'item_brands': [
                        {
                            'brand_id': 10,
                            'brand_name': 'Brand 10',
                            'item_price': 45.0,
                            'max_quantity': 14,
                            'min_quantity': 10
                        },
                        {
                            'brand_id': 60,
                            'brand_name': 'Brand 60',
                            'item_price': 295.0,
                            'max_quantity': 64,
                            'min_quantity': 60
                        }
                    ],
                    'item_description': 'This is the Item',
                    'item_id': 10,
                    'item_name': 'Item 10',
                    'order_details': {
                        'brand_id': 10,
                        'delivered_quantity': 9,
                        'is_out_of_stock': False,
                        'item_price': 45.0,
                        'ordered_quantity': 11
                    }
                },
                {
                    'item_brands': [
                        {
                            'brand_id': 30,
                            'brand_name': 'Brand 30',
                            'item_price': 145.0,
                            'max_quantity': 34,
                            'min_quantity': 30
                        },
                        {
                            'brand_id': 80,
                            'brand_name': 'Brand 80',
                            'item_price': 395.0,
                            'max_quantity': 84,
                            'min_quantity': 80
                        }
                    ],
                    'item_description': 'This is the Item',
                    'item_id': 30,
                    'item_name': 'Item 30',
                    'order_details': None
                },
                {
                    'item_brands': [
                        {
                            'brand_id': 50,
                            'brand_name': 'Brand 50',
                            'item_price': 245.0,
                            'max_quantity': 54,
                            'min_quantity': 50
                        },
                        {
                            'brand_id': 100,
                            'brand_name': 'Brand 100',
                            'item_price': 495.0,
                            'max_quantity': 104,
                            'min_quantity': 100
                        }
                    ],
                    'item_description': 'This is the Item',
                    'item_id': 50,
                    'item_name': 'Item 50',
                    'order_details': None
                }
            ],
            'section_description': 'This is Section',
            'section_id': 10,
            'section_name': 'section 10'
        }
    ],
    'total_cost': 495.0,
    'total_items': 11
}

snapshots['TestCase02GetFormDetailsAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '1394',
        'Content-Length'
    ],
    'content-type': [
        'Content-Type',
        'text/html; charset=utf-8'
    ],
    'vary': [
        'Accept-Language, Origin, Cookie',
        'Vary'
    ],
    'x-frame-options': [
        'SAMEORIGIN',
        'X-Frame-Options'
    ]
}

snapshots['TestCase02GetFormDetailsAPITestCase::test_case form_id'] = 10

snapshots['TestCase02GetFormDetailsAPITestCase::test_case form_name'] = 'Form 10'

snapshots['TestCase02GetFormDetailsAPITestCase::test_case form_description'] = 'This is the Form of Form 10'

snapshots['TestCase02GetFormDetailsAPITestCase::test_case close_date'] = '2020-06-26 17:23:01'

snapshots['TestCase02GetFormDetailsAPITestCase::test_case total_cost'] = 495.0

snapshots['TestCase02GetFormDetailsAPITestCase::test_case total_items'] = 11

snapshots['TestCase02GetFormDetailsAPITestCase::test_case sections'] = [
    {
        'item_details': [
            {
                'item_brands': [
                    {
                        'brand_id': 10,
                        'brand_name': 'Brand 10',
                        'item_price': 45.0,
                        'max_quantity': 14,
                        'min_quantity': 10
                    },
                    {
                        'brand_id': 60,
                        'brand_name': 'Brand 60',
                        'item_price': 295.0,
                        'max_quantity': 64,
                        'min_quantity': 60
                    }
                ],
                'item_description': 'This is the Item',
                'item_id': 10,
                'item_name': 'Item 10',
                'order_details': {
                    'brand_id': 10,
                    'delivered_quantity': 9,
                    'is_out_of_stock': False,
                    'item_price': 45.0,
                    'ordered_quantity': 11
                }
            },
            {
                'item_brands': [
                    {
                        'brand_id': 30,
                        'brand_name': 'Brand 30',
                        'item_price': 145.0,
                        'max_quantity': 34,
                        'min_quantity': 30
                    },
                    {
                        'brand_id': 80,
                        'brand_name': 'Brand 80',
                        'item_price': 395.0,
                        'max_quantity': 84,
                        'min_quantity': 80
                    }
                ],
                'item_description': 'This is the Item',
                'item_id': 30,
                'item_name': 'Item 30',
                'order_details': None
            },
            {
                'item_brands': [
                    {
                        'brand_id': 50,
                        'brand_name': 'Brand 50',
                        'item_price': 245.0,
                        'max_quantity': 54,
                        'min_quantity': 50
                    },
                    {
                        'brand_id': 100,
                        'brand_name': 'Brand 100',
                        'item_price': 495.0,
                        'max_quantity': 104,
                        'min_quantity': 100
                    }
                ],
                'item_description': 'This is the Item',
                'item_id': 50,
                'item_name': 'Item 50',
                'order_details': None
            }
        ],
        'section_description': 'This is Section',
        'section_id': 10,
        'section_name': 'section 10'
    }
]

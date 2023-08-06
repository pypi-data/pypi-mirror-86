# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01GetOrderDetailsOfFormAPITestCase::test_case status'] = 200

snapshots['TestCase01GetOrderDetailsOfFormAPITestCase::test_case body'] = {
    'form_id': '1',
    'order_details': [
        {
            'cost_incurred_for_item': 0.0,
            'is_out_of_stock': True,
            'item_id': 1,
            'item_name': 'Item 1',
            'quantity_added_for_item': 2,
            'quantity_received_for_item': 0
        }
    ],
    'total_cost_incurred': 0.0,
    'total_items_count': 2,
    'total_received_items_count': 0
}

snapshots['TestCase01GetOrderDetailsOfFormAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '278',
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

snapshots['TestCase01GetOrderDetailsOfFormAPITestCase::test_case form_id'] = '1'

snapshots['TestCase01GetOrderDetailsOfFormAPITestCase::test_case ordered_details'] = [
    {
        'cost_incurred_for_item': 0.0,
        'is_out_of_stock': True,
        'item_id': 1,
        'item_name': 'Item 1',
        'quantity_added_for_item': 2,
        'quantity_received_for_item': 0
    }
]

snapshots['TestCase01GetOrderDetailsOfFormAPITestCase::test_case cost_incurred'] = 0.0

snapshots['TestCase01GetOrderDetailsOfFormAPITestCase::test_case total_items_count'] = 2

snapshots['TestCase01GetOrderDetailsOfFormAPITestCase::test_case received_items_count'] = 0

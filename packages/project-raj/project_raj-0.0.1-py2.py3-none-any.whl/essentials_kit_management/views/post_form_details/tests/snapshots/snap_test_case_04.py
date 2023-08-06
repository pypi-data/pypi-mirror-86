# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase04PostFormDetailsAPITestCase::test_case status'] = 201

snapshots['TestCase04PostFormDetailsAPITestCase::test_case body'] = b''

snapshots['TestCase04PostFormDetailsAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '0',
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

snapshots['TestCase04PostFormDetailsAPITestCase::test_case user_id_for_item_1'] = 1

snapshots['TestCase04PostFormDetailsAPITestCase::test_case item_id_1'] = 1

snapshots['TestCase04PostFormDetailsAPITestCase::test_case brand_id_for_item_1'] = 1

snapshots['TestCase04PostFormDetailsAPITestCase::test_case ordered_quantity_for_item_1'] = 1

snapshots['TestCase04PostFormDetailsAPITestCase::test_case delivered_quantity_for_item_1'] = 0

snapshots['TestCase04PostFormDetailsAPITestCase::test_case is_out_of_stock_for_item_1'] = True

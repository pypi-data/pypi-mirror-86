# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01GetFormsAsListAPITestCase::test_case status'] = 200

snapshots['TestCase01GetFormsAsListAPITestCase::test_case body'] = {
    'forms': [
        {
            'close_date': '2020-07-05 04:05:01',
            'cost_incurred': 0.0,
            'estimated_cost': 0.0,
            'expected_delivery_date': '2020-08-09 02:03:01',
            'form_description': 'This is the Form of Form 1',
            'form_id': 1,
            'form_name': 'Form 1',
            'form_status': 'CLOSED',
            'items_count': 2,
            'items_pending': 2
        },
        {
            'close_date': '2020-06-26 17:23:01',
            'cost_incurred': 0,
            'estimated_cost': 0,
            'expected_delivery_date': None,
            'form_description': 'This is the Form of Form 2',
            'form_id': 2,
            'form_name': 'Form 2',
            'form_status': 'CLOSED',
            'items_count': 0,
            'items_pending': 0
        },
        {
            'close_date': '2020-10-06 04:05:01',
            'cost_incurred': 0,
            'estimated_cost': 0,
            'expected_delivery_date': None,
            'form_description': 'This is the Form of Form 3',
            'form_id': 3,
            'form_name': 'Form 3',
            'form_status': 'CLOSED',
            'items_count': 0,
            'items_pending': 0
        },
        {
            'close_date': '2020-06-05 04:05:01',
            'cost_incurred': 0,
            'estimated_cost': 0,
            'expected_delivery_date': None,
            'form_description': 'This is the Form of Form 4',
            'form_id': 4,
            'form_name': 'Form 4',
            'form_status': 'CLOSED',
            'items_count': 0,
            'items_pending': 0
        },
        {
            'close_date': '2020-07-05 04:05:01',
            'cost_incurred': 0,
            'estimated_cost': 0,
            'expected_delivery_date': None,
            'form_description': 'This is the Form of Form 5',
            'form_id': 5,
            'form_name': 'Form 5',
            'form_status': 'CLOSED',
            'items_count': 0,
            'items_pending': 0
        }
    ],
    'forms_count': 20
}

snapshots['TestCase01GetFormsAsListAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '1361',
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

snapshots['TestCase01GetFormsAsListAPITestCase::test_case forms'] = [
    {
        'close_date': '2020-07-05 04:05:01',
        'cost_incurred': 0.0,
        'estimated_cost': 0.0,
        'expected_delivery_date': '2020-08-09 02:03:01',
        'form_description': 'This is the Form of Form 1',
        'form_id': 1,
        'form_name': 'Form 1',
        'form_status': 'CLOSED',
        'items_count': 2,
        'items_pending': 2
    },
    {
        'close_date': '2020-06-26 17:23:01',
        'cost_incurred': 0,
        'estimated_cost': 0,
        'expected_delivery_date': None,
        'form_description': 'This is the Form of Form 2',
        'form_id': 2,
        'form_name': 'Form 2',
        'form_status': 'CLOSED',
        'items_count': 0,
        'items_pending': 0
    },
    {
        'close_date': '2020-10-06 04:05:01',
        'cost_incurred': 0,
        'estimated_cost': 0,
        'expected_delivery_date': None,
        'form_description': 'This is the Form of Form 3',
        'form_id': 3,
        'form_name': 'Form 3',
        'form_status': 'CLOSED',
        'items_count': 0,
        'items_pending': 0
    },
    {
        'close_date': '2020-06-05 04:05:01',
        'cost_incurred': 0,
        'estimated_cost': 0,
        'expected_delivery_date': None,
        'form_description': 'This is the Form of Form 4',
        'form_id': 4,
        'form_name': 'Form 4',
        'form_status': 'CLOSED',
        'items_count': 0,
        'items_pending': 0
    },
    {
        'close_date': '2020-07-05 04:05:01',
        'cost_incurred': 0,
        'estimated_cost': 0,
        'expected_delivery_date': None,
        'form_description': 'This is the Form of Form 5',
        'form_id': 5,
        'form_name': 'Form 5',
        'form_status': 'CLOSED',
        'items_count': 0,
        'items_pending': 0
    }
]

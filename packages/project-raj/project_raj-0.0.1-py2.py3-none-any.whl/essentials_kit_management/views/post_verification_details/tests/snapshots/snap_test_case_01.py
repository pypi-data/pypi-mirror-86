# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01PostVerificationDetailsAPITestCase::test_case status'] = 400

snapshots['TestCase01PostVerificationDetailsAPITestCase::test_case body'] = {
    'http_status_code': 400,
    'res_status': 'INVALID_VALUE_EXCEPTION',
    'response': 'Please send valid value for amount'
}

snapshots['TestCase01PostVerificationDetailsAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '116',
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

snapshots['TestCase01PostVerificationDetailsAPITestCase::test_case http_status_code'] = 400

snapshots['TestCase01PostVerificationDetailsAPITestCase::test_case res_status'] = 'INVALID_VALUE_EXCEPTION'

snapshots['TestCase01PostVerificationDetailsAPITestCase::test_case response'] = 'Please send valid value for amount'

# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase02LoginAPITestCase::test_case status'] = 401

snapshots['TestCase02LoginAPITestCase::test_case body'] = {
    'http_status_code': 401,
    'res_status': 'INVALID_PASSWORD_EXCEPTION',
    'response': 'Please send valid password'
}

snapshots['TestCase02LoginAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '111',
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

snapshots['TestCase02LoginAPITestCase::test_case http_status_code'] = 401

snapshots['TestCase02LoginAPITestCase::test_case res_status'] = 'INVALID_PASSWORD_EXCEPTION'

snapshots['TestCase02LoginAPITestCase::test_case response'] = 'Please send valid password'

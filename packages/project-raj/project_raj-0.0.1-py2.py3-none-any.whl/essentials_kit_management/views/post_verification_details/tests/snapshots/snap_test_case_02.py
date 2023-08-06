# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case status'] = 201

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case body'] = b''

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case header_params'] = {
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

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case transaction_id'] = 1

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case payment_transaction_id'] = 'string'

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case transaction_type'] = 'PHONE_PAY'

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case credit_amount'] = 100.0

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case debit_amount'] = 0.0

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case transaction_date'] = GenericRepr('FakeDatetime(2020, 6, 7, 9, 5, 4)')

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case screenshot_url'] = 'string'

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case remarks'] = ''

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case verification_status'] = None

snapshots['TestCase02PostVerificationDetailsAPITestCase::test_case user_id'] = 1

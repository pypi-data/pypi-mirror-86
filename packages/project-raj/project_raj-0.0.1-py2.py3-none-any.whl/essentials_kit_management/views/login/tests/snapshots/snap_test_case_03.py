# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase02LoginAPITestCase::test_case status'] = 200

snapshots['TestCase02LoginAPITestCase::test_case body'] = {
    'access_token': 'j3nu3SVLFBwl578WPeoJh3zed0YLjO',
    'expires_in': '2337-05-18 05:36:34.506841',
    'refresh_token': 'EvEu5Za9Z3bkQrNFgsSaYzPCOXw4Eq',
    'user_id': 1
}

snapshots['TestCase02LoginAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '159',
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

snapshots['TestCase02LoginAPITestCase::test_case user_id'] = 1

snapshots['TestCase02LoginAPITestCase::test_case access_token'] = 'j3nu3SVLFBwl578WPeoJh3zed0YLjO'

snapshots['TestCase02LoginAPITestCase::test_case expires_in'] = '2337-05-18 05:36:34.506841'

snapshots['TestCase02LoginAPITestCase::test_case refresh_token'] = 'EvEu5Za9Z3bkQrNFgsSaYzPCOXw4Eq'

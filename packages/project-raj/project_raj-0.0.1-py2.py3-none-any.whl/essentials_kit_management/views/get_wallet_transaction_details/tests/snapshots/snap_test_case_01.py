# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01GetWalletTransactionDetailsAPITestCase::test_case status'] = 200

snapshots['TestCase01GetWalletTransactionDetailsAPITestCase::test_case body'] = {
    'transaction_details': [
        {
            'credit_amount': 0.0,
            'debit_amount': 0.0,
            'remarks': 'Nothing',
            'transaction_date': '27 June 2020',
            'transaction_id': 1,
            'verification_status': None
        },
        {
            'credit_amount': 100.0,
            'debit_amount': 0.0,
            'remarks': 'Nothing',
            'transaction_date': '27 June 2020',
            'transaction_id': 2,
            'verification_status': None
        },
        {
            'credit_amount': 200.0,
            'debit_amount': 0.0,
            'remarks': 'Nothing',
            'transaction_date': '27 June 2020',
            'transaction_id': 3,
            'verification_status': None
        },
        {
            'credit_amount': 300.0,
            'debit_amount': 0.0,
            'remarks': 'Nothing',
            'transaction_date': '27 June 2020',
            'transaction_id': 4,
            'verification_status': None
        },
        {
            'credit_amount': 400.0,
            'debit_amount': 0.0,
            'remarks': 'Nothing',
            'transaction_date': '27 June 2020',
            'transaction_id': 5,
            'verification_status': None
        }
    ],
    'wallet_balance': 43500.0
}

snapshots['TestCase01GetWalletTransactionDetailsAPITestCase::test_case header_params'] = {
    'content-language': [
        'Content-Language',
        'en'
    ],
    'content-length': [
        '825',
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

snapshots['TestCase01GetWalletTransactionDetailsAPITestCase::test_case transaction_details'] = [
    {
        'credit_amount': 0.0,
        'debit_amount': 0.0,
        'remarks': 'Nothing',
        'transaction_date': '27 June 2020',
        'transaction_id': 1,
        'verification_status': None
    },
    {
        'credit_amount': 100.0,
        'debit_amount': 0.0,
        'remarks': 'Nothing',
        'transaction_date': '27 June 2020',
        'transaction_id': 2,
        'verification_status': None
    },
    {
        'credit_amount': 200.0,
        'debit_amount': 0.0,
        'remarks': 'Nothing',
        'transaction_date': '27 June 2020',
        'transaction_id': 3,
        'verification_status': None
    },
    {
        'credit_amount': 300.0,
        'debit_amount': 0.0,
        'remarks': 'Nothing',
        'transaction_date': '27 June 2020',
        'transaction_id': 4,
        'verification_status': None
    },
    {
        'credit_amount': 400.0,
        'debit_amount': 0.0,
        'remarks': 'Nothing',
        'transaction_date': '27 June 2020',
        'transaction_id': 5,
        'verification_status': None
    }
]

snapshots['TestCase01GetWalletTransactionDetailsAPITestCase::test_case wallet_balance'] = 'wallet_balance'

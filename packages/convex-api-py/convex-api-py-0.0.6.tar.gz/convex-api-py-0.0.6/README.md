# Convex API

![](https://github.com/Convex-Dev/convex-api-py/workflows/testing/badge.svg)

[Documentation](https://convex-dev.github.io/convex-api-py)

### Quick Start

First you need to download the Convex-API-py package from the python package index PyPi.

    pip install convex-api

You can now access the convex network, and get a balance from an existing account on the network by doing the following:

    >>> from convex_api import ConvexAPI
    >>> convex = ConvexAPI('https://convex.world')
    >>> convex.get_balance('0x7E66429CA9c10e68eFae2dCBF1804f0F6B3369c7164a3187D6233683c258710f')
    524786120

You can create a new emtpy account, with now balance:

    >>> from convex_api import Account
    >>> account = Account.create_new()
    >>> print(account.address_checksum)
    0x6F0e5f252B31Dc78d460Dd301ab571F47f8Bb0d7557Afff8D26A12655Dc2F6aF

You can request some funds to the new account and then get the account information:

    >>> convex.request_funds(1000000, account)
    1000000
    >>> convex.get_account_info(account)
    {'environment': {}, 'address': '6f0e5f252b31dc78d460dd301ab571f47f8bb0d7557afff8d26a12655dc2f6af', 'is_library': False, 'is_actor': False, 'memory_size': 8, 'balance': 1000000, 'allowance': 0, 'sequence': 0, 'type': 'user'}

You can export the accounts private key encoded as PKCS8 encrypt the key with a password:

    >>> account.export_to_text('secret')
    '-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIGbMFcGCSqGSIb3DQEFDTBKMCkGCSqGSIb3DQEFDDAcBAiMY42UY4PXHAICCAAw\nDAYIKoZIhvcNAgkFADAdBglghkgBZQMEASoEEJpwDMicGbGj2iSJesktIVYEQBsp\nKMTAHzvUyw8jZRr8WSrmxH7938sjma8XWI6lgd9jwTZzcGamog7p3zatw0Wp+jFK\nKruWAZmIqhBZ/2ezDv8=\n-----END ENCRYPTED PRIVATE KEY-----\n'

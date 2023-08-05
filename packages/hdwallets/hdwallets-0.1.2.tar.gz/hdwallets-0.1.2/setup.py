# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hdwallets']

package_data = \
{'': ['*']}

install_requires = \
['ecdsa>=0.14.0']

setup_kwargs = {
    'name': 'hdwallets',
    'version': '0.1.2',
    'description': 'Python implementation of the BIP32 key derivation scheme',
    'long_description': '[![PyPI version](https://img.shields.io/pypi/v/hdwallets)](https://pypi.org/project/hdwallets)\n[![Build Status](https://github.com/hukkinj1/hdwallets/workflows/Tests/badge.svg?branch=master)](https://github.com/hukkinj1/hdwallets/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)\n[![codecov.io](https://codecov.io/gh/hukkinj1/hdwallets/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkinj1/hdwallets)\n\n# hdwallets\n\nA basic implementation of the [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki) specification for hierarchical deterministic wallets.\n\nA fork of https://github.com/darosior/python-bip32 with some notable changes:\n\n- [`base58`](https://pypi.org/project/base58/) dependency removed.\n  All interfaces input and output raw bytes instead of base58 strings.\n- Replaced [`coincurve`](https://pypi.org/project/coincurve/) dependency with [`ecdsa`](https://pypi.org/project/ecdsa/)\n- Distributes type information ([PEP 561](https://www.python.org/dev/peps/pep-0561/))\n\n## Usage\n\n```python\n>>> import base58\n>>> from hdwallets import BIP32, HARDENED_INDEX\n>>> bip32 = BIP32.from_seed(bytes.fromhex("01"))\n# Specify the derivation path as a list ...\n>>> bip32.get_xpriv_from_path([1, HARDENED_INDEX, 9998])\nb"\\x04\\x88\\xad\\xe4\\x037\\x01)\\x0f\\x00\\x00\'\\x0e7\\xf9\\xe7)\\x8dCJ\\x8b\\xfb\\xc2j#\\xeb\\xc0++\\xdf}I\\x80\\xdfr\\xef6\\xad0\\xf7K\\x0ceE\\xea\\x00\\xb3D8\\x0b\\x0e\\xf4-\\x9a\\xe6\\x91\\xe9\\x82\\xe8\\xbf\\x9a\\x97\\x15\\xfe?\\x17\\xdc[\\xf7\\xc5\\xfb?\\xbezaz\\\\\\xb9"\n# ... Or in usual m/the/path/\n>>> bip32.get_xpriv_from_path("m/1/0\'/9998")\nb"\\x04\\x88\\xad\\xe4\\x037\\x01)\\x0f\\x00\\x00\'\\x0e7\\xf9\\xe7)\\x8dCJ\\x8b\\xfb\\xc2j#\\xeb\\xc0++\\xdf}I\\x80\\xdfr\\xef6\\xad0\\xf7K\\x0ceE\\xea\\x00\\xb3D8\\x0b\\x0e\\xf4-\\x9a\\xe6\\x91\\xe9\\x82\\xe8\\xbf\\x9a\\x97\\x15\\xfe?\\x17\\xdc[\\xf7\\xc5\\xfb?\\xbezaz\\\\\\xb9"\n>>> bip32.get_xpub_from_path([HARDENED_INDEX, 42])\nb"\\x04\\x88\\xb2\\x1e\\x02\\x11\\xd4\\xbb(\\x00\\x00\\x00*\\xaf?\\xc3\\x1bb)\\x1d\\x9e$\\x91\\xda\\xc2b\\x8e\\x1fm\\x7f6\\x8c(\\x8e\'2.\\x99-\\xf2\\xa1\\x83\\xd7F\\x18\\x03bB\\xb0\\xe5\\x0b\\xb8$\\x97\\xf0\\xf3\\xe47\\xea\\xd6\\xd4\\xa0\\xe3~-#\\xbf\\t\\xf5\\x19\\xb7\\xd1\\x06b\\xb0\\xac\\xc5\\xd4"\n# You can also use "h" or "H" to signal for hardened derivation\n>>> bip32.get_xpub_from_path("m/0h/42")\nb"\\x04\\x88\\xb2\\x1e\\x02\\x11\\xd4\\xbb(\\x00\\x00\\x00*\\xaf?\\xc3\\x1bb)\\x1d\\x9e$\\x91\\xda\\xc2b\\x8e\\x1fm\\x7f6\\x8c(\\x8e\'2.\\x99-\\xf2\\xa1\\x83\\xd7F\\x18\\x03bB\\xb0\\xe5\\x0b\\xb8$\\x97\\xf0\\xf3\\xe47\\xea\\xd6\\xd4\\xa0\\xe3~-#\\xbf\\t\\xf5\\x19\\xb7\\xd1\\x06b\\xb0\\xac\\xc5\\xd4"\n# You can use pubkey-only derivation\n>>> bip32 = BIP32.from_xpub(base58.b58decode_check("xpub6AKC3u8URPxDojLnFtNdEPFkNsXxHfgRhySvVfEJy9SVvQAn14XQjAoFY48mpjgutJNfA54GbYYRpR26tFEJHTHhfiiZZ2wdBBzydVp12yU"))\n>>> bip32.get_xpub_from_path([42, 43])\nb\'\\x04\\x88\\xb2\\x1e\\x04\\xf4p\\xd4>\\x00\\x00\\x00+h\\xcf\\xc2\\xd1\\xbe\\x0c\\\\-:\\x9fpDy\\\\x\\xd5E\\xc1\\x988\\xb1\\xe2X\\xd1\\xba\\xb1\\xeac\\x96\\xb04\\x8f\\x02\\xaf?<\\xbe>\\x92\\xcc\\xc1fq~\\xa9\\xcd\\xcb\\x10\\xd5\\x15]K\\xd6\\x10+\\xdb\\xa8\\xb4\\xedo\\xd2hc\\xf9x\'\n>>> bip32.get_xpub_from_path("m/42/43")\nb\'\\x04\\x88\\xb2\\x1e\\x04\\xf4p\\xd4>\\x00\\x00\\x00+h\\xcf\\xc2\\xd1\\xbe\\x0c\\\\-:\\x9fpDy\\\\x\\xd5E\\xc1\\x988\\xb1\\xe2X\\xd1\\xba\\xb1\\xeac\\x96\\xb04\\x8f\\x02\\xaf?<\\xbe>\\x92\\xcc\\xc1fq~\\xa9\\xcd\\xcb\\x10\\xd5\\x15]K\\xd6\\x10+\\xdb\\xa8\\xb4\\xedo\\xd2hc\\xf9x\'\n>>> bip32.get_pubkey_from_path("m/1/1/1/1/1/1/1/1/1/1/1")\nb\'\\x02\\x0c\\xac\\n\\xa8\\x06\\x96C\\x8e\\x9b\\xcf\\x83]\\x0c\\rCm\\x06\\x1c\\xe9T\\xealo\\xa2\\xdf\\x195\\xebZ\\x9b\\xb8\\x9e\'\n```\n\n## Installation\n\n```sh\npip install hdwallets\n```\n\n## Interface\n\nAll public keys below are compressed.\n\nAll `path` below are a list of integers representing the index of the key at each depth.\n\n#### BIP32\n\n##### from\\_seed(seed)\n\n__*staticmethod*__\n\nInstantiate from a raw seed (as `bytes`). See\n[bip-0032\'s master key generation](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#master-key-generation).\n\n##### from\\_xpriv(xpriv)\n\n__*staticmethod*__\n\nInstantiate with an encoded serialized extended private key (as `str`) as master.\n\n##### from\\_xpub(xpub)\n\n__*staticmethod*__\n\nInstantiate with an encoded serialized extended public key (as `str`) as master.\n\nYou\'ll only be able to derive unhardened public keys.\n\n##### get\\_extended\\_privkey\\_from\\_path(path)\n\nReturns `(chaincode (bytes), privkey (bytes))` of the private key pointed by the path.\n\n##### get\\_privkey\\_from\\_path(path)\n\nReturns `privkey (bytes)`, the private key pointed by the path.\n\n##### get\\_extended\\_pubkey\\_from\\_path(path)\n\nReturns `(chaincode (bytes), pubkey (bytes))` of the public key pointed by the path.\n\nNote that you don\'t need to have provided the master private key if the path doesn\'t include an index `>= HARDENED_INDEX`.\n\n##### get\\_pubkey\\_from\\_path(path)\n\nReturns `pubkey (bytes)`, the public key pointed by the path.\n\nNote that you don\'t need to have provided the master private key if the path doesn\'t include an index `>= HARDENED_INDEX`.\n\n##### get\\_xpriv\\_from\\_path(path)\n\nReturns `xpriv (str)` the serialized and encoded extended private key pointed by the given path.\n\n##### get\\_xpub\\_from\\_path(path)\n\nReturns `xpub (str)` the serialized and encoded extended public key pointed by the given path.\n\nNote that you don\'t need to have provided the master private key if the path doesn\'t include an index `>= HARDENED_INDEX`.\n\n##### get\\_master\\_xpriv(path)\n\nEquivalent to `get_xpriv_from_path([])`.\n\n##### get\\_master\\_xpub(path)\n\nEquivalent to `get_xpub_from_path([])`.\n',
    'author': 'hukkinj1',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/hdwallets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

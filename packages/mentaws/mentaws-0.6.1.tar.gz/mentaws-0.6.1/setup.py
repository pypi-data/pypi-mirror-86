# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mentaws']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'boto3>=1.14.20,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'coveralls>=1.11.1,<2.0.0',
 'cryptography>=2.9.2,<3.0.0',
 'keyring>=21.4.0,<22.0.0',
 'python-coveralls>=2.9.3,<3.0.0']

entry_points = \
{'console_scripts': ['mentaws = mentaws.main:main', 'mts = mentaws.main:main']}

setup_kwargs = {
    'name': 'mentaws',
    'version': '0.6.1',
    'description': 'moMENTary AWS credentials',
    'long_description': "\n# mentaws (moMENTary AWS tokens)\n\nStay Fresh!\n\n[![Coverage Status](https://coveralls.io/repos/github/keithrozario/mentaws/badge.svg?branch=release)](https://coveralls.io/github/keithrozario/mentaws?branch=release) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/keithrozario/mentaws.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/keithrozario/mentaws/context:python)\n\n[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)\n[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)\n[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)\n\n## Introduction\n\nmentaws (rhymes with jaws, and sounds like the candy) replaces your aws credentials file with fresh temporary tokens, while keeping your long lived AWS secret keys encrypted.\n\nThis way, the plaintext credentials file has only temporary tokens. Leaving sensitive long lived keys encrypted in your keychain.\n\n## Usage\n\n### Setup\n\n    $ mentaws setup\n    The following 4 were added to mentaws:\n    \n    👷🏿 Profile\n     1.default\n     2.mentaws1\n     3.mentaws2\n     4.mentaws3\n\n### Refresh\n\n    $ mentaws refresh\n    Generating temporary tokens...\n\n    👷🏿 Profile                    🌎 Region:            ⏰ Tokens expire at\n       default                       ap-southeast-1        Tue 19:27 tz:+08\n       mentaws1                      ap-southeast-1        Tue 19:27 tz:+08\n       mentaws2                      ap-southeast-1        Tue 19:27 tz:+08\n       mentaws3                      ap-southeast-1        Tue 19:27 tz:+08\n    \n    You're ready to go 🚀🚀\n\n### Remove a profile\n\n    $ mentaws remove default\n    Are you sure you want to delete default? (y/n): y\n    Profile default was deleted\n\n### Status\n\n    $ mentaws status\n    👷🏿 Profile                    🔑 Key:                  ⏰ Tokens expire at\n       default                       ASIA42EXAMPLE1234567    Mon 14:28 tz:+08\n       mentaws1                      ASIA42EXAMPLE1234567    Mon 14:28 tz:+08\n       mentaws2                      ASIA42EXAMPLE1234567    Mon 16:28 tz:+08\n       mentaws3                      ASIA42EXAMPLE1234567    Tue 20:28 tz:+08\n       metawsFail                    ERROR                   ***FAILED***\n       testassumptionprofile         -                       No Token Expiry\n\n## Installation\n\nThe simplest way to install mentaws is to use `pipx`\n\n    $ pipx install mentaws\n\nof `pip`\n\n    $ pip install mentaws\n\n## Adding profiles\n\nFor now, the easiest way to add a profile is to use the generic aws-cli commands:\n\n    $ aws configure --profile produser\n    AWS Access Key ID [None]: AKIAI44QH8DHBEXAMPLE\n    AWS Secret Access Key [None]: je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY\n    Default region name [None]: us-east-1\n    Default output format [None]: text\n\nOn the next `refresh`, mentaws will load these new profiles into its database. \n\n*Note: This method works even if you modified the credentials file manually.*\n\n## Implementation details\n\nThe AWS credentials are stored in a sqlite3 database in the same directory as your AWS directory.\n\nWhen you first setup mentaws, an encryption key is randomly generated and stored in your macOS keychain. This key is then used to encrypt the `aws_secret_access_key`. All other fields,including the `aws_access_key_id` are stored in plaintext -- the encrypted key together with other metadata is stored in a SQLITE database in your default aws directory.\n\nFor the encryption we use the [pyca/cryptography](https://cryptography.io/en/latest/fernet.html#implementation) package, which implements the following:\n\n* AES in CBC mode with a 128-bit key for encryption; using PKCS7 padding.\n* HMAC using SHA256 for authentication.\n* Initialization vectors are generated using os.urandom().\n\nWe store the randomly generated key in your macOS keychain using keyring, this has one limitation, namely:\n\n* Any Python script or application can access secrets created by keyring from that same Python executable without the operating system prompting the user for a password. **To cause any specific secret to prompt for a password every time it is accessed, locate the credential using the Keychain Access application, and in the Access Control settings, remove Python from the list of allowed applications.**\n\nAlthough, on my machine with macOS Catalina installed, I do get prompted once for every sensitive mentaws operation.\n\n## Warning\n\nThis project is still in beta, and work with all AWS features, use at your own risk.\n\n## Limitation\n\nBecause of the way tokens work, any operation on iam, e.g. iam:GetRole, will fail with mentaws because we do not use MFA for the authorization. \n",
    'author': 'keithrozario',
    'author_email': 'keith@keithrozario.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/keithrozario/mentaws',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mobile_payments']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome>=3.9.9,<4.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'mobile-payments',
    'version': '0.1.1',
    'description': 'Mobile payments integrations made easy.',
    'long_description': "# Mobile Payments\n\nAn easy way to integrate mobile payments into your web project.\n\n## Installation\n\n```bash\npip install mobile-payments\n```\n\n## Prerequisites\nPython 3.6+\n\n## Examples\n\n### Customer to Business payment via vodacom m-pesa\n```python\n# vodacom M-PESA\nfrom mobile_payments.vodacom import MPESA\n\napi_key = '<your-api-key>'\npublic_key = '<open-api-public-key>'\n\nm_pesa = MPESA(api_key=api_key, public_key=public_key)\n\n# Customer to Business payment\nparameters = {\n    'input_Amount': 10, # amount to be charged\n    'input_Country': 'TZN',\n    'input_Currency': 'TZS',\n    'input_CustomerMSISDN': '000000000001',\n    'input_ServiceProviderCode': '000000',\n    'input_ThirdPartyConversationID': 'c9e794e10c63479992a8b08703abeea36',\n    'input_TransactionReference': 'T23434ZE3',\n    'input_PurchasedItemsDesc': 'Shoes',\n}\n\nresponse = m_pesa.c2b(parameters)\n```\n\nSample response\n\n```\n'body': {'output_ResponseCode': 'INS-0',\n'output_ResponseDesc': 'Request processed successfully',\n'output_TransactionID': '79eKKNrYVfCj',\n'output_ConversationID': 'c9e794e10c63479992a8b08703abeea36', 'output_ThirdPartyConversationID': 'asv02e5958774f7ba228d83d0d689761'}\n```\n\n## License\nCode released under [MIT LICENSE](https://github.com/ZendaInnocent/mobile-payments/blob/main/LICENSE)\n",
    'author': 'Innocent Zenda',
    'author_email': 'zendainnocent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ZendaInnocent/mobile-payments.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

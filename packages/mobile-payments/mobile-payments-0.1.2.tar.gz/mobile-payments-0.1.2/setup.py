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
    'version': '0.1.2',
    'description': 'Mobile payments integrations made easy.',
    'long_description': "# Mobile Payments\nAn easy way to integrate mobile payments into your web project.\n\n## Motivation\nRecently, VodaCom has released open API portal for M-Pesa. The following are some issues arose:\n\nFor Python integration, they have provided the package in zipped format. It is not user friendly and some developers found it challenging in installation.\n\nAlso, the sample code provided for Python implementation are long and most comprise repitition and become prone to errors for developers.\n\nMobile Payments package try to resolve above issues for Python by providing easy and user friendly installation, also the refactored code that is simplified.\n\n\n## Installation\nInstall the package using `pip`\n```\npip install mobile-payments\n```\n\nThe package comprise both original open API codes and refactored codes.\n\nTo use original open API code import `open_api` module\n\n```\nfrom mobile_payments.open_api import APIContext, APIMethodType, APIRequest\n```\n\nTo use refactored code import `MPESA` from `vodacom` module.\n\n```\nfrom mobile_payments.vodacom import MPESA\n```\n\n\n## Prerequisites\nPython 3.6+\n\n## Examples\nThe following examples requires `api key`. It can be obtained by registering to [open api portal](https://openapiportal.m-pesa.com) and follow the instructions.\n\nIt also uses refactored code, if you want to use original open API code it is also possible but follow the examples in documentation.\n\n### Customer to Business payment via vodacom m-pesa\n\n```\n# vodacom M-PESA\nfrom mobile_payments.vodacom import MPESA\n\napi_key = '<your-api-key>'\npublic_key = '<open-api-public-key>'\n\nm_pesa = MPESA(api_key=api_key, public_key=public_key)\n\n# Customer to Business payment\nparameters = {\n    'input_Amount': 10, # amount to be charged\n    'input_Country': 'TZN',\n    'input_Currency': 'TZS',\n    'input_CustomerMSISDN': '000000000001',\n    'input_ServiceProviderCode': '000000',\n    'input_ThirdPartyConversationID': 'c9e794e10c63479992a8b08703abeea36',\n    'input_TransactionReference': 'T23434ZE3',\n    'input_PurchasedItemsDesc': 'Shoes',\n}\n\nresponse = m_pesa.customer2business(parameters)\n```\n\nSample response\n\n```\n{'body': {'output_ResponseCode': 'INS-0',\n'output_ResponseDesc': 'Request processed successfully',\n'output_TransactionID': '79eKKNrYVfCj',\n'output_ConversationID': 'c9e794e10c63479992a8b08703abeea36', 'output_ThirdPartyConversationID': 'asv02e5958774f7ba228d83d0d689761'}}\n```\n\n# Integrating in Django\nIf doing web project using Django framework\n\n```python\n# views.py\nfrom mobile_payments.vodacom import MPESA\n\ndef payments(request):\n    if request.method == 'POST':\n        form = PaymentForm(request.POST)\n        if form.is_valid():\n            m_pesa = MPESA(api_key, public_key)\n\n            parameters = {\n                'input_Amount': 10,\n                'input_Country': 'TZN',\n                'input_Currency': 'TZS',\n                # '000000000001' - phone number for testing,\n                'input_CustomerMSISDN': request.POST.get('phone'),\n                'input_ServiceProviderCode': '000000',\n                'input_ThirdPartyConversationID': get_random_string(18),\n                'input_TransactionReference': get_random_string(18),\n                'input_PurchasedItemsDesc': 'Shoes',\n            }\n\n            results = m_pesa.customer2business(parameters)\n\n            if results.body['output_ResponseCode'] == 'INS-0':\n                # successful transaction\n\n            else:\n                # unsuccessful transaction\n\n```\nMore details on response codes, see [api documentation](https://openapiportal.m-pesa.com/api-documentation)\n\n## License\nCode released under [MIT LICENSE](https://github.com/ZendaInnocent/mobile-payments/blob/main/LICENSE)\n",
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

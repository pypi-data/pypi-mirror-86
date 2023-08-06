# Mobile Payments
An easy way to integrate mobile payments into your web project.

## Motivation
Recently, VodaCom has released open API portal for M-Pesa. The following are some issues arose:

For Python integration, they have provided the package in zipped format. It is not user friendly and some developers found it challenging in installation.

Also, the sample code provided for Python implementation are long and most comprise repitition and become prone to errors for developers.

Mobile Payments package try to resolve above issues for Python by providing easy and user friendly installation, also the refactored code that is simplified.


## Installation
Install the package using `pip`
```
pip install mobile-payments
```

The package comprise both original open API codes and refactored codes.

To use original open API code import `open_api` module

```
from mobile_payments.open_api import APIContext, APIMethodType, APIRequest
```

To use refactored code import `MPESA` from `vodacom` module.

```
from mobile_payments.vodacom import MPESA
```


## Prerequisites
Python 3.6+

## Examples
The following examples requires `api key`. It can be obtained by registering to [open api portal](https://openapiportal.m-pesa.com) and follow the instructions.

It also uses refactored code, if you want to use original open API code it is also possible but follow the examples in documentation.

### Customer to Business payment via vodacom m-pesa

```
# vodacom M-PESA
from mobile_payments.vodacom import MPESA

api_key = '<your-api-key>'
public_key = '<open-api-public-key>'

m_pesa = MPESA(api_key=api_key, public_key=public_key)

# Customer to Business payment
parameters = {
    'input_Amount': 10, # amount to be charged
    'input_Country': 'TZN',
    'input_Currency': 'TZS',
    'input_CustomerMSISDN': '000000000001',
    'input_ServiceProviderCode': '000000',
    'input_ThirdPartyConversationID': 'c9e794e10c63479992a8b08703abeea36',
    'input_TransactionReference': 'T23434ZE3',
    'input_PurchasedItemsDesc': 'Shoes',
}

response = m_pesa.customer2business(parameters)
```

Sample response

```
{'body': {'output_ResponseCode': 'INS-0',
'output_ResponseDesc': 'Request processed successfully',
'output_TransactionID': '79eKKNrYVfCj',
'output_ConversationID': 'c9e794e10c63479992a8b08703abeea36', 'output_ThirdPartyConversationID': 'asv02e5958774f7ba228d83d0d689761'}}
```

# Integrating in Django
If doing web project using Django framework

```python
# views.py
from mobile_payments.vodacom import MPESA

def payments(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            m_pesa = MPESA(api_key, public_key)

            parameters = {
                'input_Amount': 10,
                'input_Country': 'TZN',
                'input_Currency': 'TZS',
                # '000000000001' - phone number for testing,
                'input_CustomerMSISDN': request.POST.get('phone'),
                'input_ServiceProviderCode': '000000',
                'input_ThirdPartyConversationID': get_random_string(18),
                'input_TransactionReference': get_random_string(18),
                'input_PurchasedItemsDesc': 'Shoes',
            }

            results = m_pesa.customer2business(parameters)

            if results.body['output_ResponseCode'] == 'INS-0':
                # successful transaction

            else:
                # unsuccessful transaction

```
More details on response codes, see [api documentation](https://openapiportal.m-pesa.com/api-documentation)

## License
Code released under [MIT LICENSE](https://github.com/ZendaInnocent/mobile-payments/blob/main/LICENSE)

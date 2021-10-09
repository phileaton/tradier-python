# Tradier-Python

Tradier-python is a python client for interacting with the Tradier API.


## Getting Started

You will need a Tradier account token which you can download from your account after logging in. 

The client also takes an optional default_account_id which can make it easier to get information if you only have one account. 

The default endpoint points to the sandbox. You will need to set the endpoint to the brokerage endpoint for live use. 

Reference documentation for the API can be found here: 

https://documentation.tradier.com/brokerage-api/overview/market-data

### Installing

pip install tradier-python

### Exmple

```
from tradier_python import TradierAPI

token = os.environ["TRADIER_TOKEN"]
account_id = os.environ["TRADIER_ACCOUNT_ID"]
t = TradierAPI(token=token, default_account_id=account_id)

profile = t.get_profile()
print(profile)
```


## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details


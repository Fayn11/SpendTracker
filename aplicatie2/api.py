
# import json
# import requests
#
# url = "https://v6.exchangerate-api.com/v6/fbae84ab721a2260065add5b/latest/EUR"
#
# payload = {}
# headers = {
#   'Autorization': 'Token fbae84ab721a2260065add5b'
# }
#
# response = requests.request("GET", url, headers=headers, data=payload)
#
# print(response.text)

# print(response.json()['conversion_rates'])

"""deconectam cand folosim api"""
import json
import requests


def get_exchange_rates():
    url = "https://v6.exchangerate-api.com/v6/fbae84ab721a2260065add5b/latest/EUR"
    payload = {}
    headers = {
      'Autorization': 'Token fbae84ab721a2260065add5b'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()['conversion_rates']

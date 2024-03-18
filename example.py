import json
from urllib import request

url = "http://127.0.0.1:8000/py/annual_exceedance?b_part=C_CAA003_SWP"

response = request.urlopen(url)
payload = json.load(response)

print(payload)

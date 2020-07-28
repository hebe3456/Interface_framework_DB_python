import requests
from utils.log import *


# take one request for example to check the request method、request_body type to make sure it works
url = ""
request_body = {
}

info(type(request_body))
res = requests.post(url=url, json=request_body)
info(res)
# INFO <Response [200]>
info(res.status_code)
# INFO 200
info(res.content)

info(res.text)

info(res.json())




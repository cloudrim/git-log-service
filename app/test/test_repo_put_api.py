import requests
from datetime import datetime
import json

location = ""
dt = datetime.now()
body = json.dumps({"last_update": dt.strftime('%Y%m%d%H%M%S'),
                   "status": "running"
                   })

r = requests.put('http://127.0.0.1:5000/repo/2', data=body)
print(r.text)

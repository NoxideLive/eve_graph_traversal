#Actions Available

After loading is complete the following actions can be run.

##System to System Navigation
This will return the vertex path for the shortest route between two systems

```python
import requests
import json

url = "http://localhost:8000/navigator/navigate/system_to_system/"

payload = json.dumps({
  "systemFrom": 30000138,
  "systemTo": 30002790
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

##Station to System Navigation
This will return the vertex path for the shortest route between a station and the destination system
```python
import requests
import json

url = "http://localhost:8000/navigator/navigate/station_to_system/"

payload = json.dumps({
  "stationFrom": 60014434,
  "systemTo": 30002790
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```
import requests, json
import pprint
data = {
    "image_url":input(),
}
headers = {'Content-type': 'application/json'}
data = requests.post("http://ec2-18-216-89-211.us-east-2.compute.amazonaws.com:5000/search", headers=headers, data=json.dumps(data)).json()
#data = requests.post("http://localhost:5000/search", headers=headers, data=json.dumps(data)).json()
pprint.PrettyPrinter(indent=1).pprint(data)

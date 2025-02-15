from http import client
import json


class Contact:
    def __init__(self, id, firstname, lastname, phone):
        self.id = id
        self.first_name = firstname
        self.last_name = lastname
        self.phone_number = phone

    def update(self, new_firstname, new_lastname, new_phone):
        self.first_name = new_firstname
        self.last_name = new_lastname
        self.phone_number = new_phone

    def sms(self, url, line_number, api_key, phone, message):
        conn = client.HTTPSConnection(f"{url}")
        payload = json.dumps({
            "lineNumber": f"{line_number}",
            "messageText": f"{message}",
            "mobiles": [
                f"{phone}"
            ],
            "sendDateTime": None
        })
        headers = {
            'X-API-KEY': f"{api_key}",
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/v1/send/bulk", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))


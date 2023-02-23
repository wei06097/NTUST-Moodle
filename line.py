###  line.py  ###

TIMEOUT = 10
TOKEN = ""

import requests
HOST = "https://notify-api.line.me/api/notify"
HEADERS = {"Authorization": "Bearer " + TOKEN}

def testMessage():
    payload = {"message": "Python OK"}
    try:
        requests.post(HOST, headers=HEADERS, data=payload, timeout=TIMEOUT)
        print("message: testMessage succeed")
    except Exception: print("error: testMessage failed")

def sendMessage(message):
    payload = {"message": message}
    try:
        requests.post(HOST, headers=HEADERS, data=payload, timeout=TIMEOUT)
        print("message: sendMessage succeed")
    except Exception: print("error: sendMessage failed")
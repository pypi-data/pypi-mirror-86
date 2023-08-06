import requests
import json
import time


def headless(clientid, configdir):
    global authtoken
    global headlessdone
    global devicecode
    headlessdone = False
    print(clientid)
    print("Starting headless GitHub authentication")
    pog = {"client_id": clientid, "scope": "gist"}
    header = {'User-Agent': "pygisty", "Accept": "application/json"}
    r = requests.Session()
    r.params.update(pog)
    r.headers.update(header)
    request = r.post('https://github.com/login/device/code')
    body = request.text
    dat = json.loads(body)
    try:
        error = dat["error"]
        print("Error: " + error)
        print(request.url)
    except KeyError:
        devicecode = dat["device_code"]
        print("I just received a code that you should enter at https://github.com/login/device\nCode: " + dat[
            "user_code"])
        while headlessdone == False:
            try:
                poggers = {"client_id": clientid, "device_code": devicecode,
                           "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}
                s = requests.Session()
                s.params.update(poggers)
                s.headers.update(header)
                pogchamp = s.post("https://github.com/login/oauth/access_token")
                data = json.loads(pogchamp.text)
                authtoken = data["access_token"]
                print("We got the auth token!")
                accessjson = {
                    "access_token": authtoken
                }
                with open(configdir+"/access_token.json", "w") as configfile:
                    json.dump(accessjson, configfile)
                headlessdone = True
            except KeyError:
                time.sleep(5)
    return authtoken

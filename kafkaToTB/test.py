import json
import requests

TB_SERVER = "10.0.0.65"



def tb_auth(username, password):
    url = "http://{0}/api/auth/login".format(TB_SERVER)

    payload=json.dumps({"username": username, "password" : password})
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)  

    return json.loads(response.text)["token"]

def tb_get_device_by_name(name, token):
    url = "http://{0}/api/tenant/devices?deviceName={1}".format(TB_SERVER, name)

    payload={}
    headers = {
    'X-Authorization': 'Bearer {0}'.format(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)

def tb_get_device_id_by_name(name, token):
    url = "http://{0}/api/tenant/devices?deviceName={1}".format(TB_SERVER, name)

    payload={}
    headers = {
    'X-Authorization': 'Bearer {0}'.format(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)['id']['id']    

def tb_get_device_token(device_id, token):
    url = "http://{0}/api/device/{1}/credentials".format(TB_SERVER, device_id)

    payload={}
    headers = {
    'X-Authorization': 'Bearer {0}'.format(token)
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)['credentialsId']

def save_device_telemetry(device_token, data):
    url = "http://{0}/api/v1/{1}/telemetry".format(TB_SERVER, device_token)

    payload = json.dumps(data)
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)



value = {
    "device" : "dev001",
    "mesourment" : "temperature",
    "value" : 25
}

token = tb_auth("apiuser@example.com", "apipassword")
payload = {str(value['mesourment']) : float(value['value']) }
print(payload)
device_id = tb_get_device_id_by_name(value['device'],token)
print("Device_id " + device_id)
device_token = tb_get_device_token(device_id,token)
print("Device_token " + device_token)
save_device_telemetry(device_token,payload)
import os
from kafka import KafkaConsumer
import json
import requests

KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC') or print("KAFKA_TOPIC Not defined") 
KAFKA_SERVER = os.environ.get('KAFKA_SERVER') or print("KAFKA_SERVER Not defined")
TB_SERVER = os.environ.get('TB_SERVER') or print("TB_SERVER Not defined")
TB_USER = os.environ.get('TB_USER') or print("TB_USER Not defined")
TB_PASSWORD = os.environ.get('TB_PASSWORD') or print("TB_PASSWORD Not defined")
print("KAFKA_TOPIC " + KAFKA_TOPIC)
print("KAFKA_SERVER " + KAFKA_SERVER)
print("TB_SERVER " + TB_SERVER)

consumer = KafkaConsumer(
    KAFKA_TOPIC, 
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='tb-consumers')

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

for msg in consumer:
    print (msg)
    data = json.loads(msg.value)

    payload = {
        "ts" : data['ts'],
        "values" : {str(data['measurement']) : float(data['value'])}
    }
    token = tb_auth(TB_USER, TB_PASSWORD)
    device_id = tb_get_device_id_by_name(data['device'],token)
    device_token = tb_get_device_token(device_id,token)
    save_device_telemetry(device_token,payload)
    print("Data written to DB")
    
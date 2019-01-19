import requests
import json

def create_server(name,host):
    """Creating Server
    """

    server_content = {'name':name,'host':host}
    data = json.dumps(server_content)
    headers = {'Content-Type':'application/json'}
    resp = requests.post('http://127.0.0.1:5000/servers/',headers=headers,data=data)
    result = resp.json()

    return result





    

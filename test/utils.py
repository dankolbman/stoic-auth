import json

def api_headers():
    """
    Headers for json request
    """
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def make_user(client):
    resp = client.post('/user/',
                       headers=api_headers(),
                       data=json.dumps({'username': 'Dan',
                                        'email': 'dan@localhost.com',
                                        'password': '123'}))
    json_resp = json.loads(resp.data.decode('utf-8'))
    return json_resp

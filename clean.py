import json
import requests


def read_config():
    with open('config.json') as f:
        data = json.load(f)

    return data


def fetch(type, url, token=None, params=None):
    headers = {
        'user-agent': 'PeerTubeCleaner/0.0.1'
    }

    if token:
        headers['authorization'] = 'Bearer ' + token

    if type == 'GET':
        r = requests.get(url, headers=headers)
    elif type == 'POST':
        r = requests.post(url, data=params, headers=headers)
    elif type == 'DELETE':
        r = requests.delete(url, headers=headers)
    else:
        raise('No compatible request type used in fetch().')

    return r.json()


def login(host, user, pwd):
    # Get OAuth client keys
    client = fetch('GET', host + '/api/v1/oauth-clients/local')

    # Get access token
    token = fetch('POST', host + '/api/v1/users/token', None, {
        'client_id': client['client_id'],
        'client_secret': client['client_secret'],
        'grant_type': 'password',
        'response_type': 'code',
        'username': user,
        'password': pwd
    })

    # Return the token
    return token['access_token']


if __name__ == '__main__':
    print('=== THIS IS A WORK IN PROGRESS ===')

    config = read_config()

    token = login(config['host'], config['username'], config['password'])
    vids = fetch('GET', config['host'] + '/api/v1/users/me/videos', token)
    print(vids)

    print('=== THIS IS A WORK IN PROGRESS ===')

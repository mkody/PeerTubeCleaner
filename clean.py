import json
import requests


def read_config():
    # Load the config.json file in the same directory as this script
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    
    with open(config_file) as f:
        data = json.load(f)

    return data


def fetch(req_type, url, token=None, params=None):
    # Make our own header with a custom UA
    headers = {
        'user-agent': 'PeerTubeCleaner/0.0.1'
    }

    # If we have our token, add the authorization header
    if token:
        headers['authorization'] = 'Bearer ' + token

    # Now we do our requests
    if req_type == 'GET':
        r = requests.get(url, headers=headers)
    elif req_type == 'POST':
        r = requests.post(url, data=params, headers=headers)
    elif req_type == 'DELETE':
        r = requests.delete(url, headers=headers)
    else:
        raise('No compatible request type used in fetch().')

    # Directly send back the parsed JSON
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

    # Return the token directly
    return token['access_token']


if __name__ == '__main__':
    print('=== THIS IS A WORK IN PROGRESS ===')

    # Read our config file
    config = read_config()

    # Fetch our user token
    token = login(config['host'], config['username'], config['password'])
    
    # List videos
    vids = fetch('GET', config['host'] + '/api/v1/users/me/videos', token)
    
    # DEBUG: print the result
    print(vids)

    print('=== THIS IS A WORK IN PROGRESS ===')

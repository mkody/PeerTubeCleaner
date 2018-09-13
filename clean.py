import os
import time
import json
import requests
import argparse
import dateutil.parser as d_parser

from tqdm import tqdm


def read_config():
    # Load the config.json file in the same directory as this script
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

    # If there isn't a config file, return None
    if not os.path.isfile(config_file):
        return None

    with open(config_file) as f:
        data = json.load(f)

    return data


def read_args():
    parser = argparse.ArgumentParser(
        description='Clean old videos from your PeerTube account.'
    )

    group_login = parser.add_argument_group(
        'Login',
        'Those will override values in config.json if present.'
    )
    group_login.add_argument(
        '--host',
        metavar='<host>',
        type=str,
        help='the PeerTube instance (ie. https://peertu.be)'
    )
    group_login.add_argument(
        '--user',
        metavar='<user>',
        type=str,
        help='your username'
    )
    group_login.add_argument(
        '--pass',
        metavar='<pass>',
        type=str,
        dest='pwd',
        help='your password'
    )

    group_limit = parser.add_argument_group(
        'Limits',
        'Set the rules.'
    )
    group_limit.add_argument(
        '--max',
        metavar='<i>',
        type=int,
        help='maximum amount of videos to keep'
    )
    group_limit.add_argument(
        '--min',
        metavar='<i>',
        type=int,
        default=0,
        help='for --days and --dur, the minimum amount of videos to spare'
    )
    group_limit.add_argument(
        '--days',
        metavar='<d>',
        type=int,
        help='days to keep'
    )
    group_limit.add_argument(
        '--dur',
        metavar='<s>',
        type=int,
        help='overall duration in seconds to keep'
    )

    args = parser.parse_args()

    # Load config file and set args if missing
    config = read_config()
    if config:
        if not args.host:
            args.host = config['host']

        if not args.user:
            args.user = config['username']

        if not args.pwd:
            args.pwd = config['password']

    # If --max, --days and --dur are all missing, display help and quit
    if not args.max and not args.days and not args.dur:
        parser.print_help()
        print('\n\n=== ERROR: You should at least use one of these: --max, --days, --dur\n')
        exit(1)

    # If the host, username or password is missing, don't continue
    if not args.host or not args.user or not args.pwd:
        parser.print_help()
        print('\n\n=== ERROR: Create a config.json or set --host, --user and -pass\n')
        exit(2)

    # Warn that --min is useless without --days or --dur
    if not (args.days or args.dur) and args.min > 0:
        print('=== WARNING: --min is useless if not used with --days or --dur\n')

    return args


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
        return r.status_code
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
    # Read the arguments
    args = read_args()

    # Fetch our user token
    token = login(args.host, args.user, args.pwd)

    # List videos (first request)
    req = fetch('GET', args.host + '/api/v1/users/me/videos?count=100', token)

    # Saving the data
    total = req['total']
    vids = req['data']
    to_delete = []

    i = 0  # cursor
    while len(vids) < total:
        # Loop until we got every video
        i += 100
        req = fetch('GET', args.host + '/api/v1/users/me/videos?count=100&start=' + str(i), token)
        vids += req['data']

    # If we did set a maximum of vids to keep
    if args.max:
        to_delete += vids[args.max:]
        del vids[args.max:]

    # If we said how many days to keep
    if args.days:
        min_ts = time.time() - args.days * 86400
        i = 0
        d = 0

        # Skip the minimum amount if specified
        for vid in vids[args.min:]:
            date_parsed = d_parser.parse(vid['publishedAt'])

            # If this video was published before the set number of days
            # we can add it to the delete list
            if date_parsed.timestamp() < min_ts:
                to_delete.append(vid)
                del vids[i + args.min - d]
                d += 1

            i += 1

    # If we want a maximum duration of all videos
    if args.dur:
        i = 0
        t = 0

        for vid in vids:
            i += 1
            t += vid['duration']

            # If we went over the minimum count of videos to keep
            # and that we went over the max duration with that video
            if (i >= args.min) and t > args.dur:
                # Delete this video and the nexts
                to_delete += vids[i:]
                del vids[i:]
                break

    for delete in tqdm(to_delete):
        fetch('DELETE', args.host + '/api/v1/videos/' + delete['uuid'], token)

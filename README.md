# PeerTubeCleaner

> Un coup de Fertilinet sur les vieilles vidéos que l'on ne veut pas conserver.

## Requirements

- Python 3 (code written for py3.7)
- A peertube account somewhere

## Install

- Install dependencies: `$ pip install -r requirements.txt`
- Copy example config to `config.json` file and edit it
  - `host`: Where the PeerTube instance is hosted, without a trailing slash. (ie. `https://tube.kdy.ch`)
  - `username`: Your username
  - `password`: Your password

## Run

Run `clean.py` with arguments.

- `--max`: A maximum number of videos to have.
- `--days`: A number of days to keep.
- `--dur`: The maximum length (in seconds) of all videos to keep. The video crossing that limit is also deleted.
- `--min`: A minimal number of videos to leave on the channel, only with `--dur` and/or `--days`.


```bash
# Help
$ python clean.py
$ python clean.py --help

# Only keep 10 videos
$ python clean.py --max 10

# Only keep videos from the last 30 days
$ python clean.py --days 30

# Only keep videos from the last 10 days but leave at least 5
$ python clean.py --min 5 --days 10

# Only keep less than 24 hours of videos
$ python clean.py --dur 86400

# Keep at least 5 videos but delete the rest if it goes over 2 hours
$ python clean.py --min 5 --dur 7200

# Keep at least 5 videos but delete the rest if it goes over 2 hours or up to 50 videos
$ python clean.py --min 5 --max 50 --dur 18000

# Keep at least 5 videos but delete the rest if it goes over 2 hours or up to 50 videos or the ones who are over 15 days old
$ python clean.py --min 7 --max 50 --dur 18000 --days 15

# --min works only with --dur and/or --days
$ python clean.py --min 10
```

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
- `--dur`: The maximum length (in seconds) of all videos to keep. The video crossing that limit is also deleted.
- `--min`: A minimal number of videos to leave on the channel, only with `--dur`.


```bash
# Help
$ python clean.py
$ python clean.py --help

# Only keep 10 videos
$ python clean.py --max 10

# Only keep less than 24 hours of videos
$ python clean.py --dur 86400

# Keep at least 5 videos but delete the rest if it goes over 2 hours
$ python clean.py --min 5 --dur 7200

# Keep at least 7 videos but delete the rest if it goes over 2 hours or up to 50 videos
$ python clean.py --min 7 --max 50 --dur 18000

# --min works only with --dur
$ python clean.py --min 10
```

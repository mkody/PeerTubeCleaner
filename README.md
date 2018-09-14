# PeerTubeCleaner
[![Liberapay receiving](https://img.shields.io/liberapay/receives/kdy.svg)](https://liberapay.com/kdy/donate)
[![Travis Build Status](https://travis-ci.org/mkody/PeerTubeCleaner.svg?branch=master)](https://travis-ci.org/mkody/PeerTubeCleaner)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![GitHub](https://img.shields.io/github/license/mkody/PeerTubeCleaner.svg)](https://github.com/mkody/PeerTubeCleaner/blob/master/LICENSE)

> Un coup de Fertilinet sur les vieilles vidéos que l'on ne veut pas conserver.

## Requirements

- Python 3 (tested on py3.5 and py3.7)
- A peertube account somewhere

## Install

- Install dependencies: `$ pip install -r requirements.txt`
- Copy the example config file to `config.json` and edit it. _(Optional, read below how to use args for this.)_
  - `host`: Where the PeerTube instance is hosted, without a trailing slash (ie. `https://tube.kdy.ch`)
  - `username`: Your username
  - `password`: Your password

## Run

Run `clean.py` with arguments (here listed in order of priority).

- `--max`: A maximum number of videos to have.
- `--min`: A minimal number of videos to leave on the channel, only with `--dur` and/or `--days`.
- `--days`: A number of days to keep.
- `--dur`: The maximum length (in seconds) of all videos to keep. The video crossing that limit is also deleted.


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

You can also set the host and your creditentials through arguments. Those will override the values in the `config.json` (or if the file is missing or is incomplete, you need to use those).

- `--host` (ie. `https://tube.kdy.ch`)
- `--user`
- `--pass`

```bash
# Set all login values
$ python clean.py --host https://tube.kdy.ch --user myUser --pass myPass --max 30

# Use the host in the config.json but another user
$ python clean.py --user otherUser --pass otherPass --max 30
```

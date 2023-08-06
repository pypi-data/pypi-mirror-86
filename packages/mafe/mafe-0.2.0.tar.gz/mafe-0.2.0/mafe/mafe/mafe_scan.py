#! /usr/bin/env python3
__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from typing import List

import click

from mafe.scan import Scanner, TrackData, DEFAULT_STORE_EVERY


@click.command()
@click.option(
    '--base-folders', '-f', multiple=True, required=True, help='Directory to scan'
)
@click.option(
    '--tracks-csv', '-t', default='tracks.csv.bz2', help='CSV file containing tracks'
)
@click.option('--max-track-length', '-m', type=int, help='Maximum track length, in seconds')
@click.option(
    '--quiet', '-q', is_flag=True, default=False, help='Suppress warnings and progress messages'
)
@click.option(
    '--store-every', '-s', type=int, default=DEFAULT_STORE_EVERY, help='Store every n tracks'
)
def scan_folders(
        base_folders: List[str], tracks_csv: str, max_track_length: int,
        quiet: bool, store_every: int
) -> None:
    if max_track_length is not None:
        TrackData.set_max_track_duration(max_track_length)

    scanner = Scanner(tracks_csv, base_folders, quiet, store_every)
    scanner.run()

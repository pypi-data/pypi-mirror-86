#! /usr/bin/env python3
__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

import click
import pandas as pd

from mafe.process import DistanceCalculator, normalize as proc_normalize, norm_mean, Cluster
from mafe.process.pca import Reducer


@click.group()
@click.option(
    '--tracks-csv', '-t', required=True, help='CSV file containing tracks'
)
@click.option(
    '--output', '-o', required=True, help='CSV file containing distances between the tracks'
)
@click.option(
    '--verbose', '-v', is_flag=True, default=False, help='Suppress warnings and progress messages'
)
@click.pass_context
def cli(ctx, tracks_csv: str, output: str, verbose: bool):
    ctx.ensure_object(dict)
    ctx.obj['tracks_csv'] = tracks_csv
    ctx.obj['output'] = output
    ctx.obj['verbose'] = verbose


@cli.command()
@click.pass_context
def normalize(ctx) -> None:
    data = pd.read_csv(ctx.obj['tracks_csv'])
    normalized = proc_normalize(data, func=norm_mean)
    normalized.to_csv(ctx.obj['output'])


@cli.command()
@click.pass_context
def pca(ctx) -> None:
    reducer = Reducer(ctx.obj['tracks_csv'])
    reducer.run().to_csv(ctx.obj['output'])


@cli.command()
@click.pass_context
def distance(ctx) -> None:
    calculator = DistanceCalculator(ctx.obj['tracks_csv'], ctx.obj['output'])
    calculator.run(verbose=(ctx.obj['verbose']))


@cli.command()
@click.option(
    '--num-clusters', '-n', required=True, type=int, help='Number of clusters to compute'
)
@click.pass_context
def cluster(ctx, num_clusters: int) -> None:
    clusterer = Cluster(ctx.obj['tracks_csv'])
    clusterer.run(num_clusters).to_csv(ctx.obj['output'])

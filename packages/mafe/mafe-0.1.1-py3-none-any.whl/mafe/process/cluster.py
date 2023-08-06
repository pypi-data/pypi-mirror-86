__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

from typing import Tuple

import pandas as pd
from sklearn.cluster import KMeans

from mafe.scan import TrackData


def k_means(
        tracks: pd.DataFrame, n_clusters: int = 8, max_iter: int = 300
) -> KMeans:
    kmeans = KMeans(n_clusters=n_clusters, max_iter=max_iter).fit(tracks)
    return kmeans


class Cluster:  # pylint: disable=too-few-public-methods

    def __init__(
            self, tracks_csv: str, text_cols: Tuple[str, ...] = None
    ) -> None:
        self.tracks = pd.read_csv(tracks_csv)
        self.text_cols = list(TrackData.STRING_COLUMNS) if text_cols is None else text_cols

    def run(self, n_clusters: int) -> pd.DataFrame:
        numbers_only = self.tracks.drop(self.text_cols, axis='columns').dropna(axis='columns')
        kmeans = k_means(numbers_only, n_clusters)
        self.tracks.insert(1, 'cluster', kmeans.labels_, True)
        return self.tracks

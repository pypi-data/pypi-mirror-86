# Music Audio Feature Extractor

## Installation
```shell script
$ pip install mafe
```

## Typical usages
```shell script
# scan music tracks to extract raw set of features
$ scan -f [MUSIC_DIR] -t scanned.csv.bz2
# run normalization on extracted features
$ process -t scanned.csv.bz2 -o normalized.csv.bz2 normalize
# create table of distances between tracks
$ process -t normalized.csv.bz2 -o distances.csv.bz2 distance
# find clusters of similar tracks
$ process -t normalized.csv.bz2 -o clustered.csv.bz2 cluster -n 4
# run dimensionality reduction, keeping only the most distinctive features
$ process -t normalized.csv.bz2 -o reduced.csv.bz2 pca
# run clustering on distinct features, creating a visualization of the clusters
$ process -t reduced.csv.bz2 -o clustered_reduced.csv.bz2 cluster -n 4 -V -I cluster.png
```

## Command line options
```shell script
$ scan --help
Usage: scan [OPTIONS]

Options:
  -f, --base-folders TEXT         Directory to scan  [required]
  -t, --tracks-csv TEXT           CSV file containing tracks
  -m, --max-track-length INTEGER  Maximum track length, in seconds
  -q, --quiet                     Suppress warnings and progress messages
  -s, --store-every INTEGER       Store every n tracks
  --help                          Show this message and exit.
$ process --help
Usage: process [OPTIONS] COMMAND [ARGS]...

Options:
  -t, --tracks-csv TEXT  CSV file containing tracks  [required]
  -o, --output TEXT      CSV file containing distances between the tracks
                         [required]

  -v, --verbose          Suppress warnings and progress messages
  --help                 Show this message and exit.

Commands:
  cluster
  distance
  normalize
  pca
```

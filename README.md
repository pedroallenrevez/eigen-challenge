[![Dagster](https://img.shields.io/badge/Python-Dagster-yellow?style=for-the-badge&logo=Python)](https://dagster.io)
[![Poetry](https://img.shields.io/badge/Python-Poetry-yellow?style=for-the-badge&logo=Python)](https://python-poetry.org/)
[![Nix](https://img.shields.io/badge/Nix-Environments-yellow?style=for-the-badge&logo=NixOS)](https://nixos.org/)
[![Standard](https://img.shields.io/badge/Nix-Standard-yellow?style=for-the-badge&logo=NixOS)](https://std.divnix.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-yellow?style=for-the-badge&logo=Docker)](https://docker.com)
[![Redis](https://img.shields.io/badge/Redis-JSON-yellow?style=for-the-badge&logo=Redis)](https://redis.com)



# Eigen Challenge 2023

## Overview

We are asked to process a set of given documents, and count meaningful occurrences of words, and their locations
in the documents.


### Goals

- Build a python package with a CLI that allows counting word occurrences in a set of documents, and allows searching for examples;
- Have proper dev environment, testing, benchmarking, and good code-conduct.
- Showcase planning, and means of communication.
- Showcase learning capabilities;
- Showcase easy dev environments with Nix.

### Non-Goals

- Losing too much time with Nix, integrating other services.

### Extra Personal Goals

1. Learn Dagster workflows (in offline environment benchmarking)
2. Learn Redis JSON and Redis-insight dashboard, as well as the redis python API

## Usage Guide

The following code is pakcaged with `poetry`, a kind of virtual environments for python.
Install poetry, and the package with:
```
$ pip install poetry
$ poetry install
```

> NOTE: Due to the application not being produced into a Python package, but instead being used inside a poetry environment, commands need to be run in the source root of the project in order to work. 

Run tests:
```
$ poetry run pytest
```

Use the CLI application:
```
$ poetry run eigen --help
Usage: eigen [OPTIONS] COMMAND [ARGS]...                                                                     
                                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell.   │
│                                                              [default: None]                               │
│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to   │
│                                                              copy it or customize the installation.        │
│                                                              [default: None]                               │
│ --help                                                       Show this message and exit.                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│ count           Calculates word-count of a set of documents on given path.                                 │
│ download        Downloads NLTK dependencies: `punkt` and `stopwords`.                                      │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

To run the CLI application do:
```
$ poetry run eigen download 
$ poetry run eigen count dev output --most-common 5 --example-sentences 3 --strategy nltk|scikit|spacy
```

## Usage Guide - Dagster

To run dagster, after installation just do:
```
$ poetry run dagster dev
```
and go to http://localhost:3000, and click `Materialize All`.

NOTE: It should be ran in the root of the project in order to work, to simplify things.


## Stack

The whole stack is comprised of two components:

- `python`
  - `typer` for CLI, and command line niceties
  - `nltk` for the main processing flow
  - `spacy` and `scikit` for benchmarking solutions
  - `dagster` for running distributed workflows

- development environment
  - `black`, `isort` and `treefmt` (included in the Nix devshell environment presets)
  - `pytest` for testing
  - `poetry` for building the package

## Detailed Design and Implementation details.

The main steps of execution are the following:
1. Document loading;
2. (Per document) Document preprocessing, sentence tokenization (separate document into it's sentences, that will be used to localize the search terms);
3. (Per document) Word tokenization and preprocessing (punctuation and stopwords (i.e. and, or, all) will be skipped);
4. (Per document) Word Counting and localization in document, and sentence index;
5. Aggregate word counts and localizations;
6. Search for most common terms. Select random sentences and highlight the term in the sentence;
7. Output example;


### Solution 1: NLTK
By using `nltk.tokenize.word_tokenize` and `nltk.tokenize.sent_tokenize` you can use their NLP engine to parse different sentences within a document, and the words contained in it.
By using the stopwords and punctuation model of NLTK you can parse out meaningless words like "all", "and", "is" that do not pose value for counting word occurrences.
After this parsing is done, we can preprocess the word tokens by normalizing them to a state where a token is case-insensitive, so "American" would equal "american".

### Solution 2: spacy

By using spacy's NLP engine API, you can process a whole document and have a processed document API, which is a different approach to NLTK, that isolates each processing step.
Preprocessing word tokens is also done with this spacy object, with no need to download any different models like NLTK, reducing the needed dependencies.
All in all, due to this overwhelming engine, processing takes much more time, which you can confer by the benchmarking results below.


### Benchmark: scikit-learn.CountVectorizer

As a baseline solution we use `scikit.CountVectorizer`, which ended up being the fastest
solution, due to the C-bindings implementation of scikit.
Although it ended up being the most noisy and ugly solution, needing a better parsing step than the vectorizer allowed to select tokens, which is highly simplified by both `nltk` and `spacy` API.
We have to manually build our WordCounter, and thus the implemented solution is not as readable.

### Time Benchmarks

| Scikit | Spacy | NLTK |
| ------ | ----- | ---- |
| 0.15s  | 6s    | 0.30s|


### Dagster and Redis interaction

In the learning experience of Dagster, the objective was to follow the basic tutorial and implement a basic solution that would emulate a real-time system. The following happens:
1. Every minute a document is added onto the `input` folder;
2. A Scheduled Dagster job is ran every minute to consume the document, where word counts are made;
3. The resulting preprocessed document is added onto the Redis JSON database, as well as the counter;
4. If a counter already exists, it's values are updated with the new stream.

> NOTE: Database interaction is made through the Dagster `asset` API, which might not be the best approach. Instead we could use an IOManager that would interact with the database, but I looked no further into the topic.

To test this interaction you should run:
```
$ docker-compose up -d
$ poetry run eigen dagster-ingest
```
You can check the results at `localhost:3000` for the Dagster dashboard, and at `localhost:8001` for redis-insight dashboard, where you can check the objects added onto the database.

## Notes on Nix

In this project there are some `*.nix` files. Nix is a new technology - a functional package manager. Nix is also a declarative language.
It allows declaring a system-definition, with almost mathematical soundness. It is used in this project to manage development environment, and produces some files like `treefmt.yml` that belong to the development experience. Other files included in this:
- `comb/QUEEN/devshells.nix`
- `flake.nix`, `flake.lock`

You can install the development environment by first installing Nix and then running the script `activate.sh`.
It is not needed for running this project, and are personal files - Poetry manages the python dev environment, packaging and running the application.

## Learning Conclusions

- `dagster`
  - how to define data assets, how the graph dependency is built
  ```python
  @asset
  def asset_name():
    return 1

  @asset
  def dependent_asset(asset_name):
    return asset_name * 2
  ```
  - overall use of the interface - just click "Materialize All"
  - jobs are schedulable and encapsulate a dagster graph
  ```python
  eigen_job = define_asset_job("eigen_job", selection=AssetSelection.all())

  defs = Definitions(
      assets=all_assets,
      jobs=[eigen_job],  # Addition: add the job to Definitions object (see below)
  )
  ```
    - `AssetSelection` allows us to select assets define in our dagster definitions for a job.
    - define a job with `Definitions` and related assets
    - define a schedule for the job with, and activate the schedule programatically
    ```python
    eigen_schedule = ScheduleDefinition(
        job=eigen_job,
        cron_schedule="0 * * * *",  # every hour
        default_status=DefaultScheduleStatus.RUNNING
    )
    ```
    - defining `IOManagers` to output dagster asset artifacts
      - to filesystem using `FileSystemIOManager`
- `direnv` - a way of defining development environments based on file-system access by changing directory to the folder, it activates the environment. How to properly set it up on a non-NixOs Linux distribution:
  - write a config file at `~/.config/nix/nix.conf` with:
  ```
  experimental-features = nix-command flakes
  keep-derivations = true
  keep-outputs = true
  ```
  - activation of the environment when using divnix/std methodology (check repo badges for more information)
- `nix` environments and how to properly set up a python environment that uses C bindings:
  - it would throw an error because nix environments are isolated, and not linked to system installed libraries;
  - define the following environment variables on the divnix/std wrapper around numtide/devshells by linking to the nix store dependencies of C compiler, and other utilities like zlib compression (used by scipy):
  ```nix
  env = [
    {
      # Link to libstc++ libraries, and zlib libraries
      name = "LD_LIBRARY_PATH";
      value = ''${nixpkgs.stdenv.cc.cc.lib}/lib/:${nixpkgs.zlib}/lib/:$LD_LIBRARY_PATH'';
    }
  ];
  ```
- `ruff` tested and used ruff to lint the codebase, instead of `autoflake8` which ended up being much faster.
- `redis.json` - how to use redis JSON database to store documents, and redis-insight to inspect the database
  - look at `eigen/db.py` for a simple API demonstration

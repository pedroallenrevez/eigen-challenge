[![Dagster](https://img.shields.io/badge/Python-Dagster-yellow?style=for-the-badge&logo=Python)](https://dagster.io)
[![Poetry](https://img.shields.io/badge/Python-Poetry-yellow?style=for-the-badge&logo=Python)](https://python-poetry.org/)
[![Nix](https://img.shields.io/badge/Nix-Environments-yellow?style=for-the-badge&logo=NixOS)](https://nixos.org/)
[![Standard](https://img.shields.io/badge/Nix-Standard-yellow?style=for-the-badge&logo=NixOS)](https://std.divnix.com/)



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
$ poetry run eigen count dev/ --most-common 5 --example-sentences 3
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


### Benchmark 1: scikit-learn.TF-IDF

### Benchmark 2: spacy

### Solution: NLTK

### Timers

| Scikit | Spacy | NLTK |
| ------ | ----- | ---- |
| 0.15s  | 6s    | 0.30s|



## Notes on Nix

In this project there are some `*.nix` files. Nix is a new technology - a functional package manager. Nix is also a declarative language.
It allows declaring a system-definition, with almost mathematical soundness. It is used in this project to manage development environment, and produces some files like `treefmt.yml` that belong to the development experience. Other files included in this:
- `comb/QUEEN/devshells.nix`
- `flake.nix`, `flake.lock`

You can install the development environment by first installing Nix and then running the script `activate.sh`.
It is not needed for running this project, and are personal files - Poetry manages the python dev environment, packaging and running the application.

## Conclusions

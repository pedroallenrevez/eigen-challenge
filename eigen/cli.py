import operator
import random
import string
from enum import Enum
from functools import reduce, partial
from pathlib import Path
from time import time
from typing import Dict, Tuple

import typer
import nltk

from .nlp import WordCounter, count_nltk, count_scikit, count_spacy
from .output import build_output_table, search, read_sentence

app = typer.Typer()


class Strategy(str, Enum):
    SPACY = "spacy"
    NLTK = "nltk"
    SCIKIT = "scikit"


STRATEGY_FN = {
    Strategy.SPACY: count_spacy,
    Strategy.NLTK: count_nltk,
    Strategy.SCIKIT: count_scikit,
}

@app.command()
def download():
    """Downloads NLTK dependencies: `punkt` and `stopwords`."""
    nltk.download("punkt")
    nltk.download("stopwords")

@app.command()
def count(
    path: Path,
    most_common: int = 5,
    example_sentences: int = 3,
    strategy: Strategy = Strategy.NLTK,
):
    """Calculates word-count of a set of documents on given path."""
    assert path.is_dir(), "Provided path has to be a directory with documents."
    counts = []
    fn = STRATEGY_FN[strategy]
    (path / "processed").mkdir(exist_ok=True)
    for p in path.glob("*.txt"):
        doc = p.read_text(encoding="utf-8")
        cnt, sentences = fn(p.name, doc)
        counts.append(cnt)
        # write temporary documents
        out_fp = (path / "processed" / p.name).open("w")
        for s in sentences:
            out_fp.write(s + "\n")
        out_fp.close()
    # gather all WordCounters into one
    sum_counter: WordCounter = reduce(operator.add, counts, WordCounter())

    outputs = search(
        partial(read_sentence, (path / "processed")),
        sum_counter, most_common, example_sentences
    )
    # build the output table
    table = build_output_table(outputs)


def main():
    app()


if __name__ == "__main__":
    main()

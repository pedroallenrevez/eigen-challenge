import operator
import os
import shutil
import time
from enum import Enum
from functools import partial, reduce
from pathlib import Path
from typing import Optional

import nltk
import typer
from loguru import logger

from .nlp import WordCounter, count_nltk, count_scikit, count_spacy
from .output import build_output_table, read_sentence, search

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
    """Downloads NLTK dependencies: `punkt` and `stopwords`.
    Also downloads spacy english language model."""
    nltk.download("punkt")
    nltk.download("stopwords")
    os.system("poetry run python -m spacy download en_core_web_sm")


@app.command()
def dagster_ingest():
    """Every 1-minute adds a document to the input folder, to be ingested by dagster.
    Dagster as a scheduled job that runs every minute, that will consume the document,
    make the counts and add it onto a database and update the overall count values.
    """
    os.system("poetry run dagster dev &")
    os.system("rm input/*")
    last_name: Optional[Path] = None
    for p in Path("./dev").glob("*.txt"):
        print(f"Adding {p.name} to input folder. Waiting 1minute....")
        if last_name is not None:
            os.system(f"rm {last_name.as_posix()}")
        last_name = Path("./input") / p.name
        shutil.copy(p, last_name)
        time.sleep(60)


@app.command()
def count(
    input_path: Path,
    output_path: Path,
    most_common: int = 5,
    example_sentences: int = 3,
    strategy: Strategy = Strategy.NLTK,
):
    """Calculates word-count of a set of documents on given path."""
    start_time = time.time()
    assert (
        input_path.is_dir() and output_path.is_dir()
    ), "Provided paths have to be a directory with documents."
    counts = []
    fn = STRATEGY_FN[strategy]
    for p in input_path.glob("*.txt"):
        doc = p.read_text(encoding="utf-8")
        cnt, sentences = fn(p.name, doc)
        counts.append(cnt)
        # Write temporary documents
        (output_path / strategy.value).mkdir(exist_ok=True)
        out_fp = (output_path / strategy.value / p.name).open("w")
        for s in sentences:
            out_fp.write(s + "\n")
        out_fp.close()
    # Gather all WordCounters into one
    sum_counter: WordCounter = reduce(operator.add, counts, WordCounter())

    outputs = search(
        partial(read_sentence, (output_path / strategy.value)),
        sum_counter,
        most_common,
        example_sentences,
    )
    # Build the output table
    build_output_table(outputs)
    end_time = time.time()
    logger.warning(f"Took {end_time - start_time} seconds.")


def main():
    app()


if __name__ == "__main__":
    main()

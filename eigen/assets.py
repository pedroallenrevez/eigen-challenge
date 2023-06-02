from pathlib import Path
import operator
from functools import reduce
from typing import Callable

from dagster import Dict, List, MetadataValue, Output, asset, Tuple

from .nlp import WordCounter, count_nltk, count_scikit, count_spacy
from .output import build_output_table, search, SearchOutput


@asset
def load_documents() -> Dict[str, str]:
    """Returns a set of documents that are read from an input folder.

    NOTE: Only works with file-system access, on a development deployment of dagster,
    for testing purposes.

    Returns:
        Dict[str, str]: A set of documents and corresponding name.
    """
    docs = {}
    for p in Path("./input").glob("*.txt"):
        doc = p.read_text(encoding="utf-8")
        docs[p.name] = doc
    return docs


def count_ocurrences(load_documents: Dict[str, str], fn: Callable) -> Tuple[WordCounter, Dict[str, List[str]]]:
    """Counts the occurrences in a set of provided documents, given a provided processing function.

    Args:
        load_documents (Dict[str, str]): A set of documents and corresponding names.
        fn (Callable): The processing function to count words.

    Returns:
        Tuple[WordCounter, Dict[str, List[str]]]: A WordCounter, and a set of named documents, and preprocessed sentences.
    """
    doc_sents = {}
    counters = []
    for doc_name, doc in load_documents.items():
        counter, sentences = fn(doc_name, doc)
        counters.append(counter)
        doc_sents[doc_name] = sentences
    sum_counter: WordCounter = reduce(operator.add,counters, WordCounter())
    return (sum_counter, doc_sents)

@asset
def count_ocurrences_nltk(load_documents: Dict[str, str]) -> Tuple[WordCounter, Dict[str, List[str]]]:
    """NLTK version of `count_occurrences`.

    Check `count_occurrences` for more details.

    Args:
        load_documents (Dict[str, str]): A set of documents and corresponding names.
        fn (Callable): The processing function to count words.

    Returns:
        Tuple[WordCounter, Dict[str, List[str]]]: A WordCounter, and a set of named documents, and preprocessed sentences.
    """
    return count_ocurrences(load_documents, count_nltk)

@asset
def count_ocurrences_spacy(load_documents: Dict[str, str]) -> Tuple[WordCounter, Dict[str, List[str]]]:
    """spaCy version of `count_occurrences`.

    Check `count_occurrences` for more details.

    Args:
        load_documents (Dict[str, str]): A set of documents and corresponding names.
        fn (Callable): The processing function to count words.

    Returns:
        Tuple[WordCounter, Dict[str, List[str]]]: A WordCounter, and a set of named documents, and preprocessed sentences.
    """
    return count_ocurrences(load_documents, count_spacy)

@asset
def count_ocurrences_scikit(load_documents: Dict[str, str]) -> Tuple[WordCounter, Dict[str, List[str]]]:
    """Scikit version of `count_occurrences`.

    Check `count_occurrences` for more details.

    Args:
        load_documents (Dict[str, str]): A set of documents and corresponding names.
        fn (Callable): The processing function to count words.

    Returns:
        Tuple[WordCounter, Dict[str, List[str]]]: A WordCounter, and a set of named documents, and preprocessed sentences.
    """
    return count_ocurrences(load_documents, count_scikit)

def search_most_common(
    count_ocurrences: Tuple[WordCounter, Dict[str, List[str]]]
) -> Output[List[SearchOutput]]:
    """Runs the search algorithm to look for sentences that have the most common search terms.

    Args:
        count_ocurrences (Tuple[WordCounter, Dict[str, List[str]]]): A WordCounter and preprocessed
        sentences where terms occur.

    Returns:
        Output[List[SearchOutput]]: A set of search sentences outputs, the most common words,
        the documents where they occur, and randomly picked example sentences.
    """
    counter, sentences = count_ocurrences
    outputs = search(
        lambda doc_name, sent_idx: sentences[doc_name][sent_idx],
        counter, most_common=5, example_sentences=3
    )
    table = build_output_table(outputs)
    metadata = {
        "preview": MetadataValue.text(table),
        "most_common": 5,
        "example_sentences": 3,
    }
    return Output(
        value=outputs,
        metadata=metadata
    )


@asset
def search_most_common_nltk(
    count_ocurrences_nltk: Tuple[WordCounter, Dict[str, List[str]]]
) -> Output[List[SearchOutput]]:
    """NLTK version of the search algorithm.
    Look at `search_most_common` for more details.

    Args:
        count_ocurrences (Tuple[WordCounter, Dict[str, List[str]]]): A WordCounter and preprocessed
        sentences where terms occur.

    Returns:
        Output[List[SearchOutput]]: A set of search sentences outputs, the most common words,
        the documents where they occur, and randomly picked example sentences.
    """
    return search_most_common(count_ocurrences_nltk)

@asset
def search_most_common_spacy(
    count_ocurrences_spacy: Tuple[WordCounter, Dict[str, List[str]]]
) -> Output[List[SearchOutput]]:
    """spaCy version of the search algorithm.
    Look at `search_most_common` for more details.

    Args:
        count_ocurrences (Tuple[WordCounter, Dict[str, List[str]]]): A WordCounter and preprocessed
        sentences where terms occur.

    Returns:
        Output[List[SearchOutput]]: A set of search sentences outputs, the most common words,
        the documents where they occur, and randomly picked example sentences.
    """
    return search_most_common(count_ocurrences_spacy)

@asset
def search_most_common_scikit(
    count_ocurrences_scikit: Tuple[WordCounter, Dict[str, List[str]]]
) -> Output[List[SearchOutput]]:
    """Scikit version of the search algorithm.
    Look at `search_most_common` for more details.

    Args:
        count_ocurrences (Tuple[WordCounter, Dict[str, List[str]]]): A WordCounter and preprocessed
        sentences where terms occur.

    Returns:
        Output[List[SearchOutput]]: A set of search sentences outputs, the most common words,
        the documents where they occur, and randomly picked example sentences.
    """
    return search_most_common(count_ocurrences_scikit)
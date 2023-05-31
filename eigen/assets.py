from pathlib import Path
import operator
from functools import reduce

from dagster import Dict, List, MetadataValue, Output, asset, Tuple, op

from .nlp import WordCounter, count_nltk
from .output import build_output_table, search, SearchOutput


@asset
def load_documents() -> Dict[str, str]:
    docs = {}
    for p in Path("dev").glob("*.txt"):
        doc = p.read_text(encoding="utf-8")
        docs[p.name] = doc
    return docs


# @asset
# def preprocess_documents(load_documents: Dict[str, str]) -> Dict[str, List[str]]:
#     ndocs = {}
#     for doc_name, doc in load_documents.items():
#         ndocs[doc_name] = sent_tokenize(doc)
#     return ndocs


@asset
def count_ocurrences(load_documents: Dict[str, str]) -> Tuple[WordCounter, Dict[str, List[str]]]:
    doc_sents = {}
    counters = []
    for doc_name, doc in load_documents.items():
        counter, sentences = count_nltk(doc_name, doc)
        counters.append(counter)
        doc_sents[doc_name] = sentences
    sum_counter: WordCounter = reduce(operator.add,counters, WordCounter())
    return (sum_counter, doc_sents)


@asset
def search_most_common(
    count_ocurrences: Tuple[WordCounter, Dict[str, List[str]]]
) -> Output[List[SearchOutput]]:
    "Returns a markdown table with the top most common words"
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

@op(config_schema={"most_common": int, "example_sentences": int})
def search_most_common(
    count_ocurrences: Tuple[WordCounter, Dict[str, List[str]]]
) -> Output[List[SearchOutput]]:
    "Returns a markdown table with the top most common words"
    counter, sentences = count_ocurrences
    #table = build_output_table_dagster(sentences, counter, most_common=5, example_sentences=3)
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
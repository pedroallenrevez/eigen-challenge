import random
import string
import re
from io import StringIO
from pathlib import Path
from typing import List, Dict, Tuple, Callable
from functools import partial

from Levenshtein import distance
from rich.console import Console
from rich.table import Table
from nltk.tokenize import word_tokenize

from .nlp import WordCounter



def read_sentence(path:Path, document: str, sentence_idx: int) -> str:
    """Opens a file handle for a document and reads a specific sentence.

    NOTE: Expects preprocesed documents that were sentence tokenized.

    Args:
        path (Path): where the documents reside.
        document (str): specific document name in `path`.
        sentence_idx (int): specific example sentence index to read.

    Returns:
        str: Example sentence.
    """
    path /= document 
    with open(path, "r+", encoding="utf-8") as fp:
        for i in range(sentence_idx+1):
            s = fp.readline()
    return s

def highlight_sentence(
    sentence: str, search_term: str, black_white_output: bool = False
) -> str:
    """Searches for the `search_term` within a sentence, within constraints of the following variations:
    (assuming search term is `america` the following would match)
    1. `america,`
    2. `america.\n'
    3. `america's`
    4. `America`
    The following would NOT match:
    1. `American`

    After the term is found, it is "highlighted", with `rich` library where it is colorized,
    or wrapper in `***` in case the output is black and white.

    Uses the levenshtein distance to calculate distance between words.

    Args:
        sentence (str): the example sentence to be highlighted;
        search_term (str): the normalized search term (tokenized, lower-case);
        black_white_output (bool, optional): whether the output will be black and white,
        in which case, search_term is wrapped in `***`. Defaults to False.

    Returns:
        str: Sentence with highlighted search-term.
    """
    START_TOKEN = "***" if black_white_output else "[magenta]"
    END_TOKEN = "***" if black_white_output else "[/magenta]"

    PATTERN1 = lambda token: fr"(^| )(?i)({token})"
    PATTERN = lambda token: fr"{PATTERN1(token)}([{re.escape(string.punctuation)} ]+|\.\\n)"
    SUB_PATTERN = fr"\1{START_TOKEN}\2{END_TOKEN}\3"

    for token in word_tokenize(sentence):
        # if distance(token.lower(), search_term) == 0:
        if token.lower() == search_term:
            break

    return re.sub(PATTERN(token), SUB_PATTERN, sentence)


SearchOutput = Tuple[str, int, set, List[str]]

def search(
    fn: Callable,
    counter: WordCounter, most_common: int = 5, example_sentences: int = 3
) -> List[SearchOutput]:
    outputs = []

    for w, c in counter.most_common(most_common):
        examples = counter._localizer[w]
        doc_set = set([d for d, _ in examples])
        sents = []
        for _ in range(example_sentences):
            doc_name, sent_idx = random.choice(examples)
            sentence = fn(doc_name, sent_idx)
            assert sentence != "", (doc_name, sent_idx, w)
            sents.append(highlight_sentence(sentence, w))
            outputs.append((w, c, doc_set, sents))

    return outputs


def build_output_table(outputs: List[SearchOutput]) -> str:
    table = Table(title="Most common word occurrences.")
    table.add_column("Word", justify="right", style="cyan", no_wrap=True)
    table.add_column("Docs", style="magenta")
    table.add_column("Sentences", justify="left", style="green")
    for w, c, doc_set, sents in outputs:
        table.add_row(f"{w}({c})", str(doc_set), "".join([f"{i}. {s}\n" for i, s in enumerate(sents)]))

    console = Console()
    console.print(table)
    console = Console(file=StringIO())
    console.print(table)
    str_output = console.file.getvalue()
    return str_output
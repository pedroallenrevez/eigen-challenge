import random
import re
import string
from io import StringIO
from pathlib import Path
from typing import Callable, List, Tuple

from nltk.tokenize import word_tokenize
from rich.console import Console
from rich.table import Table

from .nlp import WordCounter

SearchOutput = Tuple[str, int, set, List[str]]


def read_sentence(path: Path, document: str, sentence_idx: int) -> str:
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
        for i in range(sentence_idx + 1):
            s = fp.readline()
    return s


def highlight_sentence(
    sentence: str, search_term: str, black_white_output: bool = False
) -> str:
    """Searches for the `search_term` within a sentence, within constraints of the
    following variations:
    (assuming search term is `america` the following would match)
    1. `america,`
    2. `america.\n'
    3. `america's`
    4. `America`
    The following would NOT match:
    1. `American`

    After the term is found, it is "highlighted", with `rich` library where it is
    colorized, or wrapper in `***` in case the output is black and white.

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

    def PATTERN1(token):
        return f"(^| )(?i)({token})"

    def PATTERN(token):
        return f"{PATTERN1(token)}([{re.escape(string.punctuation)} ]+|\\.\\\\n)"

    SUB_PATTERN = rf"\1{START_TOKEN}\2{END_TOKEN}\3"

    for token in word_tokenize(sentence):
        # if distance(token.lower(), search_term) == 0:
        if token.lower() == search_term:
            break

    return re.sub(PATTERN(token), SUB_PATTERN, sentence)


def search(
    fn: Callable,
    counter: WordCounter,
    most_common: int = 5,
    example_sentences: int = 3,
    black_white_output: bool = False,
) -> List[SearchOutput]:
    """Searches and highlights terms in a sentence, using `highlight_sentence`
    function.
    1. Queries `most_common` words from `counter` arguments;
    2. Looks for term occurrences and corresponding documents;
    3. Picks a number of `example_sentences`
    4. Highlights the term in the sentence.

    Args:
        fn (Callable): Which function to use to search for terms;
        counter (WordCounter): An object with word occurrences, with term occurrences
        in sentences.
        most_common (int, optional): the most common word occurrences. Defaults to 5.
        example_sentences (int, optional): the number of example sentences with term
        occurrence. Defaults to 3.

    Returns:
        List[SearchOutput]: A list of tuples, of (word, occurrences, set of documents,
        example sentences)
    """
    outputs = []

    for w, c in counter.most_common(most_common):
        examples = counter._localizer[w]
        doc_set = set([d for d, _ in examples])
        sents = []
        for _ in range(example_sentences):
            doc_name, sent_idx = random.choice(examples)
            sentence = fn(doc_name, sent_idx)
            assert sentence != "", (doc_name, sent_idx, w)
            sents.append(
                highlight_sentence(sentence, w, black_white_output=black_white_output)
            )
        outputs.append((w, c, doc_set, sents))

    return outputs


def build_output_table(outputs: List[SearchOutput]) -> str:
    """Builds a `rich` output table from a list of search outputs and prints it.

    Args:
        outputs (List[SearchOutput]): most common words, it's count, documents where it
        appears, and example sentences.

    Returns:
        str: A rendered table that can be printed.
    """
    table = Table(title="Most common word occurrences.")
    table.add_column("Word", justify="right", style="cyan", no_wrap=True)
    table.add_column("Docs", style="magenta")
    table.add_column("Sentences", justify="left", style="green")
    for w, c, doc_set, sents in outputs:
        table.add_row(
            f"{w}({c})",
            str(doc_set),
            "".join([f"{i}. {s}\n" for i, s in enumerate(sents)]),
        )

    console = Console()
    console.print(table)
    console = Console(file=StringIO())
    console.print(table)
    str_output = console.file.getvalue()
    return str_output

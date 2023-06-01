import nltk
import scipy
import spacy

import re
from collections import Counter

from sklearn.feature_extraction.text import CountVectorizer


import string
from typing import Any, Dict, List, Optional, Tuple

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

PUNKT = string.punctuation
# Define the regex pattern to match punctuation
RGX_PUNKT = re.escape(string.punctuation)  # + '$'
RGX_ELLIPSIS = re.escape("...")
RGX_QUOTES = re.escape("''")
RGX_DQUOTES = re.escape('""')
RGX_BACKTICK = re.escape("``")
RGX_HIFEN = re.escape("--")
RGX_EXTENDED_PUNKT = [
    RGX_PUNKT,
    RGX_ELLIPSIS,
    RGX_QUOTES,
    RGX_DQUOTES,
    RGX_BACKTICK,
    RGX_HIFEN,
]
# Combine the patterns into a single pattern

RGX_SUFFIXES = [
    re.escape("'ve"),
    re.escape("'re"),
    re.escape("'s"),
    re.escape("n't"),
    re.escape("'m"),
    re.escape("'ll"),
    re.escape("'d"),
    re.escape("'em"),
]
# RGX_PATTERN = re.compile(f'{RGX_PUNKT}|{RGX_ELLIPSIS}|{RGX_QUOTES}|{RGX_DQUOTES}|{RGX_BACKTICK}|{RGX_HIFEN}')
RGX_PATTERN = re.compile("|".join(RGX_EXTENDED_PUNKT + RGX_SUFFIXES))

Word = str
Sentence = str
# document name, sentence index
WordLoc = Tuple[str, int]
Sentences = List[Sentence]


class WordCounter:
    def __init__(self):
        self._counter = Counter()
        self._localizer: Dict[Word, List[WordLoc]] = {}

    def update(self, words: List[Word], doc_name: str, sentence_idx: int):
        """Update one time per sentence.

        Updates all word counts, and their localizations within a named document
        and the index of the sentence (these are indexed according to a document
        preprocessor).

        Args:
            words (List[Word]): Token words to be added.
            doc_name (str): From which document the words come from.
            sentence_idx (int): From which sentence index the word comes from.
        """
        self._counter.update(words)
        for w in words:
            if w in self._localizer:
                self._localizer[w].append((doc_name, sentence_idx))
            else:
                self._localizer[w] = [(doc_name, sentence_idx)]

    def most_common(self, i: int) -> List[Tuple[str, int]]:
        """Mirrors collections.Counter.most_common method.

        Args:
            i (int): _description_

        Returns:
            List[Tuple[str, int]]: _description_
        """
        return self._counter.most_common(i)

    def __add__(self, other: "WordCounter") -> "WordCounter":
        """Sums to WordCounters to join their word counts and sentence localizations.

        Args:
            other (WordCounter): The second member to add.

        Returns:
            WordCounter: A summed up WordCounter.
        """
        self._counter += other._counter
        for k, v in other._localizer.items():
            if k in self._localizer:
                self._localizer[k] = self._localizer[k] + other._localizer[k]
            else:
                self._localizer[k] = other._localizer[k]
        return self

    # def __repr__(self) -> str:
    #     return str(self._counter)


def preprocess_sentence(sentence: str) -> str:
    return sentence.replace("\n", "")


def preprocess_words_nltk(words: List[str]) -> List[str]:
    """With the help of NLTK word_tokenize we can easily separate works and punctuation.
    We then preprocess words according to the following rules:
    1. Lower-case words
    2. Remove punctuation
    3. Remove stopwords
    4. Remove apostrophe cases ('ve, 're, etc.)

    Since `word_tokenize` from nltk already separates words from punctuation like
    i.e. hard-earned, into ["hard-earned", ","], we can easily separate actual punctuation
    from word formation. Additionally, tokenizing `could've` will result in ["could", "'ve"]
    in which case we can easily detect with regex.


    Args:
        words (List[str]): Words to be filtered and processed

    Returns:
        List[str]: Clean set of tokenized meaningful words.
    """
    EN_STOPWORDS = set(stopwords.words("english"))
    clean_words = []
    for word in words:
        if (
            word not in PUNKT
            and word not in EN_STOPWORDS
            and (cword := RGX_PATTERN.sub("", word)) != ""
        ):
            clean_words.append(cword)
    return clean_words


def count_nltk(doc_name: str, document: str) -> Tuple[WordCounter, Sentences]:
    """Preprocess a unique document and apply transformations:"""
    word_counts = WordCounter()
    sentences: List[str] = sent_tokenize(document)
    fixed_sentences: List[str] = []

    for i, sent in enumerate(sentences):
        # We return the unprocessed sentences
        sent = preprocess_sentence(sent)
        fixed_sentences.append(sent)
        sent = sent.lower()
        words: List[str] = word_tokenize(sent)
        clean_words = preprocess_words_nltk(words)
        word_counts.update(clean_words, doc_name, i)

    return (word_counts, fixed_sentences)


def count_spacy(doc_name: str, document: str) -> Tuple[WordCounter, Sentences]:
    SPACY_EN = spacy.load("en_core_web_sm")
    doc: spacy.tokens.doc.Doc = SPACY_EN(document)
    word_counts = WordCounter()

    def is_token_allowed(token):
        return bool(
            token and str(token).strip() and not token.is_stop and not token.is_punct
        )

    def preprocess_token(token):
        return str(token).strip().lower()

    fixed_sentences = []
    for i, s in enumerate(doc.sents):
        fixed_sentences.append(preprocess_sentence(str(s)))
        clean_words = [preprocess_token(w) for w in s if is_token_allowed(w)]
        word_counts.update(clean_words, doc_name, i)
    return (word_counts, fixed_sentences)


# def count_scikit(documents: List[str]) -> scipy.sparse.csr_matrix:
def count_scikit(doc_name: str, document: str) -> WordCounter:
    # Create an instance of CountVectorizer
    vectorizer = CountVectorizer(
        token_pattern=r"\b\w+\b",  # Keep only words consisting of alphanumeric characters
        lowercase=True,  # Convert all words to lowercase
        stop_words="english",  # Remove stopwords
        strip_accents="unicode",  # Strip accents during preprocessing
        encoding="utf-8",  # Set encoding type
        decode_error="replace",  # Replace decoding errors
    )

    # Fit the vectorizer to the documents and transform the documents into a word-count matrix
    X = vectorizer.fit_transform([document])

    counter = Counter()
    for word, count in zip(vectorizer.get_feature_names_out(), X.toarray()[0]):
        counter[word] = count
    return counter

import re
import string

from nltk.tokenize import sent_tokenize, word_tokenize

from eigen.nlp import WordCounter, preprocess_sentence, preprocess_words_nltk


def test_sentence_select(test_document):
    sentences = sent_tokenize(test_document)
    counter = WordCounter()
    for i, s in enumerate(sentences):
        s = preprocess_sentence(s).lower()
        ws = preprocess_words_nltk(word_tokenize(s))
        counter.update(ws, "test_document", i)
    for word, locs in counter._localizer.items():
        word = preprocess_words_nltk([word])[0]
        for _, sentence_idx in locs:
            assert word in preprocess_sentence(sentences[sentence_idx]).lower()


def test_search_term():
    START_TOKEN = "***"
    END_TOKEN = "***"
    TOKEN = "america"

    PATTERN1 = lambda token: rf"(^|\s)(?i)({token})"
    SUB_PATTERN = rf"\1{START_TOKEN}\2{END_TOKEN}"
    assert bool(re.match(PATTERN1(TOKEN), " america"))
    assert bool(re.match(PATTERN1(TOKEN), " America"))
    assert bool(re.match(PATTERN1(TOKEN), "America"))
    sentence = " america "
    res = re.sub(PATTERN1(TOKEN), SUB_PATTERN, sentence)
    assert res == " ***america*** "

    PATTERN = (
        lambda token: rf"{PATTERN1(token)}([{re.escape(string.punctuation)} ]+|\.\\n)"
    )
    SUB_PATTERN = rf"\1{START_TOKEN}\2{END_TOKEN}\3"

    sentence = " america "
    res = re.sub(PATTERN(TOKEN), SUB_PATTERN, sentence)
    assert res == " ***america*** "

    sentence = " America "
    res = re.sub(PATTERN(TOKEN), SUB_PATTERN, sentence)
    assert res == " ***America*** "

    sentence = " America, "
    res = re.sub(PATTERN(TOKEN), SUB_PATTERN, sentence)
    assert res == " ***America***, "

    sentence = " America's "
    res = re.sub(PATTERN(TOKEN), SUB_PATTERN, sentence)
    assert res == " ***America***'s "

    sentence = "America's "
    res = re.sub(PATTERN(TOKEN), SUB_PATTERN, sentence)
    assert res == "***America***'s "

    sentence = " america.\n"
    res = re.sub(PATTERN(TOKEN), SUB_PATTERN, sentence)
    assert res == " ***america***.\n"

    sentence = " American "
    res = re.sub(PATTERN(TOKEN), SUB_PATTERN, sentence)
    assert res == " American "

    TOKEN = "us"
    sentence = " dangerous "
    res = re.sub(PATTERN(TOKEN), SUB_PATTERN, sentence)
    assert res == " dangerous "

    TOKEN = "iraq"
    sentence = " Iraq's "
    res = re.sub(PATTERN(TOKEN), SUB_PATTERN, sentence)
    assert res == " ***Iraq***'s "

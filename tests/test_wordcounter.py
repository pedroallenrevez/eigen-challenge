import operator
from functools import reduce

from eigen.nlp import WordCounter


def test_counter_update(test_sentences):
    counter = WordCounter()
    for i, s in enumerate(test_sentences):
        words = s.split(" ")
        counter.update(words, "test_document", i)

    assert "hello" in counter._counter
    assert counter._counter["hello"] == 3
    assert "hello" in counter._localizer
    assert counter._localizer["hello"] == [
        ("test_document", 0),
        ("test_document", 0),
        ("test_document", 0),
    ]


def test_counter_add(test_sentences):
    counter = WordCounter()
    for i, s in enumerate(test_sentences):
        words = s.split(" ")
        counter.update(words, "test_document", i)

    counter1 = WordCounter()
    words = test_sentences[0].split(" ")
    counter1.update(words, "test_document", 0)
    counter2 = WordCounter()
    words = test_sentences[1].split(" ")
    counter2.update(words, "test_document", 1)

    sum_counter: WordCounter = reduce(operator.add, [counter1, counter2], WordCounter())

    assert counter._counter == sum_counter._counter
    assert counter._localizer == sum_counter._localizer

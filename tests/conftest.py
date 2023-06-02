import pytest

from eigen.nlp import WordCounter


@pytest.fixture
def test_document():
    return ("Let me begin by saying thanks to all you who've traveled, from far and "
            "wide, to brave the cold today.  We all made this journey for a reason. "
            "It's humbling, but in my heart I know you didn't come here just for me, "
            "you came here because you believe in what this country can be. In the face"
            " of war, you believe there can be peace. In the face of despair, you "
            "believe there can be hope. In the face of a politics that's shut you out, "
            "that's told you to settle, that's divided us for too long, you believe we "
            " can be one people, reaching for what's possible, building that more "
            "perfect union.")


@pytest.fixture
def test_sentences():
    sentences = [
        "this is hello world hello hello",
        "and this is goodbye blue sky goodbye",
    ]
    return sentences


@pytest.fixture
def test_preprocess_sentences():
    sentences = [
        ("Let me begin by saying thanks to all you who've traveled, from far and wide, "
        " to brave the cold today.")
    ]
    return sentences


@pytest.fixture
def test_counter(test_sentences):
    counter = WordCounter()
    for i, s in enumerate(test_sentences):
        words = s.split(" ")
        counter.update(words, "test_document", i)
    return counter, test_sentences

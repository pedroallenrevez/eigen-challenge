from nltk.tokenize import word_tokenize

from eigen.nlp import preprocess_sentence, preprocess_words_nltk


def test_preprocessing():
    sentence1 = (
        "Let me begin by saying thanks to all you who've traveled, from far "
        "and wide, to brave the cold today."
    )
    sentence1 = preprocess_sentence(sentence1)
    sentence1 = sentence1.lower()
    words = word_tokenize(sentence1)
    assert preprocess_words_nltk(words) == [
        "let",
        "begin",
        "saying",
        "thanks",
        "traveled",
        "far",
        "wide",
        "brave",
        "cold",
        "today",
    ]

    sentence2 = (
        "And as our economy changes, let's be the generation that ensures our "
        "nation's workers are sharing in our prosperity. Let's protect the "
        "hard-earned benefits their companies have promised. Let's make it "
        "possible for hardworking Americans to save for retirement. "
        "And let's allow our unions and their organizers to lift up this "
        "country's middle-class again."
    )
    sentence2 = preprocess_sentence(sentence2)
    sentence2 = sentence2.lower()
    words = word_tokenize(sentence2)
    toks = preprocess_words_nltk(words)
    assert toks == [
        "economy",
        "changes",
        "let",
        "generation",
        "ensures",
        "nation",
        "workers",
        "sharing",
        "prosperity",
        "let",
        "protect",
        "hard-earned",
        "benefits",
        "companies",
        "promised",
        "let",
        "make",
        "possible",
        "hardworking",
        "americans",
        "save",
        "retirement",
        "let",
        "allow",
        "unions",
        "organizers",
        "lift",
        "country",
        "middle-class",
    ]

    toks = preprocess_words_nltk(["hard-earned"])
    assert toks == ["hard-earned"]

    sentence3 = "this is hard-earned sentence from u.s., testing tokens"
    sentence3 = preprocess_sentence(sentence3)
    sentence3 = sentence3.lower()
    words = word_tokenize(sentence3)
    toks = preprocess_words_nltk(words)
    assert toks == ["hard-earned", "sentence", "u.s.", "testing", "tokens"]

from word_filter.word_filter import WordFilter


def test_word_filter():
    filter = WordFilter("target_value")
    assert filter

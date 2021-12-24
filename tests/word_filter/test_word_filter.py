from word_filter.word_filter import WordFilter


def test_word_filter():
    filter = WordFilter("ng_word")
    assert filter


def test_detect():
    filter = WordFilter("ng_word")
    actual = filter.detect("hoge ng_word huga.")

    expected = True
    assert actual == expected

from word_filter.word_filter import WordFilter


def test_word_filter():
    filter = WordFilter("ng_word")
    assert filter


def test_detect_included():
    filter = WordFilter("ng_word")
    actual = filter.detect("hoge ng_word huga.")

    expected = True
    assert actual == expected


def test_detect_not_included():
    filter = WordFilter("ng_word")
    actual = filter.detect("message not included")

    expected = False
    assert actual == expected

import pytest

from word_filter.word_filter import WordFilter


def test_word_filter():
    filter = WordFilter("ng_word")
    assert filter


class TestDetect:
    @pytest.mark.parametrize(
        "ng_word, message, expected",
        [
            ("ng_word", "hoge ng_word huga.", True),
            ("ng_word", "message not included.", False),
        ],
    )
    def test_normal(self, ng_word, message, expected):
        filter = WordFilter(ng_word)
        actual = filter.detect(message)
        assert actual == expected


class TestDetectFromSnsText:
    @pytest.mark.parametrize(
        "ng_word, text, expected",
        [
            ("ng_word", "hoge: ng_word huga.", True),
            ("ng_word", "hoge: text not included.", False),
        ],
    )
    def test_normal(self, ng_word, text, expected):
        filter = WordFilter(ng_word)
        actual = filter.detect_from_sns_text(text)
        assert actual == expected

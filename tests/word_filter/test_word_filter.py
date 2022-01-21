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
            ("ng_word", "ho:ge: ng_word huga.", True),
            ("ng_word", "hoge: huga : ng_word.", True),
            ("ng_word", ":hoge: ng_word huga.", True),
            ("ng_word", "hoge:          ng_word huga.", True),
        ],
    )
    def test_normal(self, ng_word, text, expected):
        filter = WordFilter(ng_word)
        actual = filter.detect_from_sns_text(text)
        assert actual == expected

    @pytest.mark.parametrize(
        "ng_word, text",
        [
            ("ng_word", "not matching text"),  # ユーザ名がない
            ("ng_word", "hoge:ng_word huga."),  # 「:」の直後にスペースがないパターン
        ],
    )
    def test_not_match_format(self, ng_word, text):
        filter = WordFilter(ng_word)
        with pytest.raises(ValueError) as e:
            filter.detect_from_sns_text(text)
        actual = str(e.value)
        expected = f'SNS形式の文字列ではありません text: "{text}"'
        assert actual == expected

from cmath import exp

import pytest

from word_filter.word_filter import WordFilter


def test_word_filter():
    filter = WordFilter("ng_word")
    assert filter


class TestDetect:
    @pytest.mark.parametrize(
        "ng_words, message, expected",
        [
            (["ng_word"], "hoge ng_word huga.", True),
            (["ng_word"], "message not included.", False),
            (["ng_word1", "ng_word2"], "hoge ng_word1 huga.", True),
            (["ng_word1", "ng_word2"], "hoge ng_word2 huga.", True),
            (["ng_word1", "ng_word2"], "message not included.", False),
        ],
    )
    def test_normal(self, ng_words, message, expected):
        filter = WordFilter(*ng_words)
        actual = filter.detect(message)
        assert actual == expected


class TestDetectFromSnsText:
    @pytest.mark.parametrize(
        "ng_words, text, expected",
        [
            (["ng_word"], "hoge: ng_word huga.", True),
            (["ng_word"], "hoge: text not included.", False),
            (["ng_word"], "ho:ge: ng_word huga.", True),
            (["ng_word"], "hoge: huga : ng_word.", True),
            (["ng_word"], ":hoge: ng_word huga.", True),
            ([" "], "hoge: ng_word", False),
            ([" "], "hoge:  ng_word", True),  # 先頭スペースが1つがテキストに含まれるパターン
            (["ng_word1", "ng_word2"], "hoge: ng_word1 huga.", True),
            (["ng_word1", "ng_word2"], "hoge: ng_word2 huga.", True),
            (["ng_word1", "ng_word2"], "hoge: text not included.", False),
        ],
    )
    def test_normal(self, ng_words, text, expected):
        filter = WordFilter(*ng_words)
        actual = filter.detect_from_sns_message(text)
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
            filter.detect_from_sns_message(text)
        actual = str(e.value)
        expected = f'SNS形式の文字列ではありません sns_message: "{text}"'
        assert actual == expected


class TestCensor:
    @pytest.mark.parametrize(
        "ng_words, message, expected",
        [
            (["ng_word"], "hoge: huga", "hoge: huga"),
            (["ng_word"], "hoge: NG_WORD", "hoge: NG_WORD"),
            (["ng_word"], "NG_WORD: huga", "NG_WORD: huga"),
            (["NG_WORD"], "ng_word: huga", "ng_word: huga"),
            (["NG_WORD"], "hoge: ng_word", "hoge: ng_word"),
            (["ng_word1", "ng_word2"], "hoge: huga", "hoge: huga"),
        ],
    )
    def test_not_exist(self, ng_words, message, expected):
        filter = WordFilter(*ng_words)
        actual = filter.censor(message)
        assert actual == expected

    class TestExist:
        @pytest.mark.parametrize(
            "ng_words, message, expected",
            [
                (["ng_word"], "hoge: ng_word", "hoge: <censored>"),
                (["ng_word"], "hoge: ng_word ng_word", "hoge: <censored> <censored>"),
                (["ng_word1", "ng_word2"], "hoge: ng_word1", "hoge: <censored>"),
                (["ng_word1", "ng_word2"], "hoge: ng_word2", "hoge: <censored>"),
                (
                    ["ng_word1", "ng_word2"],
                    "hoge: ng_word1, ng_word2",
                    "hoge: <censored>, <censored>",
                ),
            ],
        )
        def test_in_text(self, ng_words, message, expected):
            filter = WordFilter(*ng_words)
            actual = filter.censor(message)
            assert actual == expected

        @pytest.mark.parametrize(
            "ng_word, message, expected",
            [
                ("ng_word", "ng_word: huga", "<censored>: huga"),
                ("ng_word", "ng_word_ng_word: huga", "<censored>_<censored>: huga"),
            ],
        )
        def test_in_user(self, ng_word, message, expected):
            filter = WordFilter(ng_word)
            actual = filter.censor(message)
            assert actual == expected

        def test_set_censored_text(self):
            filter = WordFilter("ng_word", censored_text="<set_cencored_text>")
            actual = filter.censor("ng_word")
            expected = "<set_cencored_text>"
            assert actual == expected

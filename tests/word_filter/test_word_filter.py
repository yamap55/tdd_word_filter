import os

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


class TestDetectFromSnsMessage:
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
            actual = filter.censor("hoge ng_word huga.")
            expected = "hoge <set_cencored_text> huga."
            assert actual == expected


class TestCensorFromSnsMessage:
    def test_normal(self):
        filter = WordFilter("ng_word")
        actual = filter.censor_from_sns_message("ng_word: ng_word huga.")
        expected = "ng_word: <censored> huga."
        assert actual == expected

    def test_not_sns_message(self):
        filter = WordFilter("ng_word")
        with pytest.raises(ValueError) as e:
            filter.censor_from_sns_message("ng_word huga.")
        actual = str(e.value)
        expected = 'SNS形式の文字列ではありません sns_message: "ng_word huga."'
        assert actual == expected


class TestCensorFromTextFile:
    # TODO: test_output_textをtmpdirを使う形式に書き換える
    # TODO: pytestのtempファイルを使用してファイルを作る
    # TODO: 複数行のテキストが含まれるファイルのテストを追加

    @pytest.fixture(autouse=True)
    def setup(self):
        self.filter = WordFilter("ng_word")

    def test_output_path(self, tmpdir):
        with open(tmpdir / "a.txt", "w") as f:
            f.write("ng_word: ng_word huga.")
        actual = self.filter.censor_from_text_file(str(tmpdir / "a.txt"))
        expected = tmpdir / "a_censored.txt"
        assert actual == expected

    def test_output_text(self):
        with open("b.txt", "w") as f:
            f.write("ng_word: ng_word huga.")
        output_path = self.filter.censor_from_text_file("b.txt")
        with open(output_path, "r") as f:
            actual = f.read()
        expected = "ng_word: <censored> huga."
        assert actual == expected
        os.remove("b.txt")
        os.remove("b_censored.txt")

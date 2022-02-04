"""ワードフィルタ"""
import re


class WordFilter:
    """ワードフィルタ"""

    """SNS形式のメッセージパターン"""
    _SNS_MESSAGE_PATTERN = re.compile(r"^(.+): (.+)")

    """検閲された文字列"""
    _CENSORED_TEXT = "<censored>"

    def __init__(self, ng_word: str):
        """
        初期化

        Parameters
        ----------
        ng_word : str
            フィルタする文字列
        """
        self.ng_word = ng_word

    def detect(self, text: str) -> bool:
        """
        フィルタする文字列が含まれているかを判定する

        Parameters
        ----------
        text : str
            判定対象のテキスト

        Returns
        -------
        bool
            含まれているか否か
        """
        return self.ng_word in text

    def detect_from_sns_message(self, sns_message: str) -> bool:
        """
        SNS形式の文字列にフィルタする文字列が含まれているかを判定する

        Parameters
        ----------
        sns_message : str
            SNS形式の文字列

        Returns
        -------
        bool
            含まれているか否か
        """
        m = self._SNS_MESSAGE_PATTERN.match(sns_message)
        if not m:
            raise ValueError(f'SNS形式の文字列ではありません sns_message: "{sns_message}"')
        return self.detect(m.group(2))

    def censor(self, text: str) -> str:
        """
        文字列にng_wordが含まれていたら検閲する

        Parameters
        ----------
        text : str
            判定対象の文字列

        Returns
        -------
        str
            検閲済み文字列

        Example
        -------
        >>> filter = WordFilter("ng_word")
        >>> filter.censor("hoge: ng_word")
        "hoge: <censored>"
        """
        if not self.detect(text):
            return text
        return text.replace(self.ng_word, self._CENSORED_TEXT)

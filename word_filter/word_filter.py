"""ワードフィルタ"""
import re


class WordFilter:
    """ワードフィルタ"""

    """SNS形式のメッセージパターン"""
    _SNS_MESSAGE_PATTERN = re.compile(r"^(.+): (.+)")

    def __init__(self, *ng_words: str, censored_text="<censored>"):
        """
        初期化

        Parameters
        ----------
        ng_words : str
            フィルタする文字列
        censored_text : str, optional
            検閲された文字列, by default "<censored>"
        """
        self.ng_words = ng_words
        self.censored_text = censored_text

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
        return any(ng_word in text for ng_word in self.ng_words)

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
        m = self._match_sns_message(sns_message)
        return self.detect(m.group(2))

    def censor(self, text: str) -> str:
        """
        文字列にng_wordが含まれていたら検閲する

        Parameters
        ----------
        text : str
            検閲対象の文字列

        Returns
        -------
        str
            検閲済み文字列

        Example
        -------
        >>> filter = WordFilter("ng_word")
        >>> filter.censor("hoge ng_word")
        "hoge <censored>"
        """
        if not self.detect(text):
            return text
        result = text
        for ng_word in self.ng_words:
            result = result.replace(ng_word, self.censored_text)
        return result

    def censor_from_sns_message(self, sns_message: str) -> str:
        """
        SNS形式の文字列にng_wordが含まれていたら検閲する

        Parameters
        ----------
        sns_message : str
            検閲対象のSNS形式のメッセージ

        Returns
        -------
        str
            検閲済みメッセージ

        Example
        -------
        >>> filter = WordFilter("ng_word")
        >>> filter.censor("ng_word: ng_word")
        "ng_word: <censored>"
        """
        m = self._match_sns_message(sns_message)
        sns_message = m.group(2)
        censored_text = self.censor(sns_message)
        return f"{m.group(1)}: {censored_text}"

    def _match_sns_message(self, sns_message: str) -> re.Match:
        """
        SNS形式のメッセージに正規表現を適用する

        Parameters
        ----------
        sns_message : str
            SNS形式のメッセージ

        Returns
        -------
        re.Match
            正規表現を適用した結果
        """
        m = self._SNS_MESSAGE_PATTERN.match(sns_message)
        if not m:
            raise ValueError(f'SNS形式の文字列ではありません sns_message: "{sns_message}"')
        return m

    def censor_from_text_file(self, input_file_path: str) -> str:
        """
        テキストファイルにng_wordが含まれていたら検閲する

        Parameters
        ----------
        input_file_path : str
            検閲対象のテキストファイルのパス

        Returns
        -------
        str
            検閲済みテキストファイルのパス

        Example
        -------
        >>> filter = WordFilter("ng_word")
        >>> filter.censor_from_text_file("input.txt")
        "input_censored.txt"
        """
        output_file_path = input_file_path.replace(".txt", "_censored.txt")
        return output_file_path

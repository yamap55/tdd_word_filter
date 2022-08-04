"""ワードフィルタ"""
import re
from functools import reduce
from pathlib import Path
from typing import Any


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

        ng_words = set(ng_words)  # type: ignore
        # 内包されているNGワード対応
        # 内包しているワードで処理をする
        # 例: 「ng_word,ng_word99」が設定されている場合にng_word99を先に処理する事で、「<censored>99」とならない
        self.ng_words = reversed(sorted(list(ng_words), key=len))
        self.censored_text = censored_text
        self._censor_history = []

    def describe(self) -> list[dict[str, Any]]:
        """
        censorの呼び出し履歴から統計を算出

        Returns
        -------
        list[dict[str, Any]]
            censorの呼び出し履歴からの統計
        """
        return self._censor_history

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
        return self._censor(text)

    def _censor(self, text: str) -> str:
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

        def f(frequency: dict[str, int], ng_word: str) -> dict[str, int]:
            count = text.count(ng_word)
            frequency[ng_word] = count
            return frequency

        frequency = reduce(f, self.ng_words, {})
        for ng_word in self.ng_words:
            result = result.replace(ng_word, self.censored_text)
        self._censor_history.append({"user_name": "", "text": text, "frequency": frequency})
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
        censored_text = self._censor(sns_message)
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

    def censor_from_text_file(self, input_file_path: Path) -> Path:
        """
        テキストファイルにng_wordが含まれていたら検閲する

        Parameters
        ----------
        input_file_path : Path
            検閲対象のテキストファイルのパス

        Returns
        -------
        Path
            検閲済みテキストファイルのパス

        Example
        -------
        >>> filter = WordFilter("ng_word")
        >>> filter.censor_from_text_file("input.txt")
        PosixPath("input_censored.txt")
        """
        replaced_file_name = f"{input_file_path.stem}_censored{input_file_path.suffix}"
        output_file_path = input_file_path.parent / replaced_file_name
        with (open(input_file_path, "r") as input, open(output_file_path, "a") as output):
            for text in input:
                censored_text = self.censor_from_sns_message(text)
                print(censored_text, file=output)

        return output_file_path

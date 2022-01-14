"""ワードフィルタ"""


class WordFilter:
    """ワードフィルタ"""

    def __init__(self, ng_word: str):
        """
        初期化

        Parameters
        ----------
        ng_word : str
            フィルタする文字列
        """
        self.ng_word = ng_word

    def detect(self, message: str) -> bool:
        """
        フィルタする文字列が含まれているかを判定する

        Parameters
        ----------
        message : str
            判定対象のメッセージ

        Returns
        -------
        bool
            含まれているか否か
        """
        return self.ng_word in message

    def detect_from_sns_text(self, text: str) -> bool:
        """
        SNS形式の文字列のメッセージにフィルタする文字列が含まれているかを判定する

        Parameters
        ----------
        text : str
            SNS形式の文字列

        Returns
        -------
        bool
            含まれているか否か
        """
        return self.detect(text.split(":")[1])

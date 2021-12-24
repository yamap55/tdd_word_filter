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
        pass

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
        return True

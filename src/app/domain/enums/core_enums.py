"""コア区分値モジュール
ドメインに依存しない区分値を定義するモジュール
"""
from enum import Enum


class LogLevel(Enum):
    """ログレベルEnumクラス
    ログレベルを定義するenumクラス
    """
    INFO = "info"
    DEBUG = "debug"


class Environment(Enum):
    """アプリケーション環境Enumクラス
    アプリケーションの実行環境を定義するenumクラス
    """
    PROD = "prod"
    LOCAL = "local"

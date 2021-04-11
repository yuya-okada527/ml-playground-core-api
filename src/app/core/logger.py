"""ロギングモジュール
アプリケーション内のログ設定を定義するモジュール
アプリケーションのログは必ずここのロガーを通してロギングする必要がある
"""
import logging
import sys

from domain.enums.core_enums import LogLevel

from core.config import CoreSettings

settings = CoreSettings()

# ------------------------
# ログフォーマット定義
# ------------------------
APP_LOG_FORMAT = "Level:%(levelname)s\tType:CoreApiApp\tTime:%(asctime)s\tFile:%(pathname)s\tMessage:%(message)s"
ACCESS_LOG_FORMAT = "Level:%(levelname)s\tType:CoreApiAccess\tTime:%(asctime)s\tProcessTime:%(process_time)s\tClient:%(client_addr)s\tMethod:%(method)s\tPath:%(path)s\tQuery:%(query)s\tStatusCode:%(status_code)s"
JSON_LOG_FORMAT = "Level:%(levelname)s\tType:%(type)s\tTime:%(asctime)s\tMessage:%(message)s"


def create_app_logger(log_name: str) -> logging.Logger:
    """アプリケーションロガー作成関数
    アプリケーションロガーを作成する
    Args:
        log_name: ロガー名
    Returns:
        logging.Logger: ロガー
    """

    return _create_logger(
        log_name=log_name,
        log_format=APP_LOG_FORMAT
    )


def create_access_logger() -> logging.Logger:
    """アクセスロガー作成関数

    Returns:
        logging.Logger: ロガー
    """
    return _create_logger(
        log_name="access_logger",
        log_format=ACCESS_LOG_FORMAT
    )


def create_json_logger() -> logging.Logger:
    """JSON形式のログメッセージを出力するロガー作成関数

    Returns:
        logging.Logger: ロガー
    """
    return _create_logger(
        log_name="json_logger",
        log_format=JSON_LOG_FORMAT
    )


def _create_logger(log_name: str, log_format: str) -> logging.Logger:
    """ロガー作成関数
    ロガーを作成する
    Args:
        log_name: ロガー名
        log_format: ログフォーマット
    Returns:
        logging.Logger: ロガー
    """
    # ロガーの作成
    log = logging.getLogger(log_name)

    # ログレベルの設定
    if settings.api_log_level == LogLevel.INFO:
        log.setLevel(logging.INFO)
    elif settings.api_log_level == LogLevel.DEBUG:
        log.setLevel(logging.DEBUG)

    # 標準出力に出力
    handler = logging.StreamHandler(stream=sys.stdout)
    # LTSV形式で出力
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    log.addHandler(handler)

    # プロパゲートしない
    log.propagate = False

    return log


# ------------------------
# 名前付きロガー定義
# ------------------------
ACCESS_LOGGER = create_access_logger()
JSON_LOGGER = create_json_logger()

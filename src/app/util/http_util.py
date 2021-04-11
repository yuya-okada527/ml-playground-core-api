"""HTTPユーティリティモジュール

HTTP通信に関するユーティリティを提供するモジュール

Todo:
    * 共通モジュールから提供する
    * バッチのモジュールをベースとする
"""
import time
from functools import wraps
from typing import Dict, Optional, Union

import requests
from core.logger import create_app_logger
from pydantic import BaseModel
from requests.exceptions import Timeout

# タイムアウト関連定数
WAIT_TIME_BASE = 5
TIMEOUT = 3

# ヘッダー関連定数
CONTENT_TYPE = "Content-Type"
APPLICATION_JSON = "application/json"

LOG = create_app_logger(__file__)


class ServerSideError(Exception):
    pass


class ClientSideError(Exception):
    pass


def retry_exec(max_retry_num: int):
    def _retry_exec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retry_num):
                try:
                    return func(*args, **kwargs)
                except ServerSideError:
                    LOG.warn("サーバーサイドエラーが発生しました。スリープ後、リトライします。")
                    time.sleep(WAIT_TIME_BASE * (i + 1))
        return wrapper
    return _retry_exec


@retry_exec(max_retry_num=3)
def call_get_api(
    url: str,
    query: Optional[BaseModel] = None,
    query_string: Optional[str] = None
):

    # リクエスト条件を構築
    if query_string:
        url += "?" + query_string
    if query:
        query = query.dict()  # type: ignore

    # API実行
    try:
        response = requests.get(url, query, timeout=TIMEOUT)
    except Timeout:
        raise ServerSideError()

    # ステータスコードをチェック
    __check_status_code(response)

    return response


def call_post_api(url: str, data: Union[str, BaseModel], headers: Dict[str, str] = None):

    # POSTデータを文字列に変換
    data_str = data.json() if isinstance(data, BaseModel) else data
    assert type(data_str) == str

    # API実行
    try:
        response = requests.post(url=url, data=data_str, timeout=TIMEOUT, headers=headers)
    except Timeout:
        raise ServerSideError()

    # ステータスコードをチェック
    __check_status_code(response)

    return response


def __check_status_code(response) -> None:
    # ステータスコードをチェック
    if response.status_code >= 500:
        raise ServerSideError()
    elif response.status_code >= 400:
        LOG.error(f"クライアントサイドエラーが発生しました。 レスポンス: {response.json()}")
        raise ClientSideError()

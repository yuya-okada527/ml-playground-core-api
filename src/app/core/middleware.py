"""ミドルウェア定義モジュール

APIの実行前後で実行される処理を定義する
"""
import time
from typing import Awaitable, Callable

from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import CoreSettings
from core.logger import create_access_logger

core_settings = CoreSettings()

access_log = create_access_logger()

# CORSミドルウェア
CORS = {
    "middleware_class": CORSMiddleware,
    "allow_origins": core_settings.fe_domain.split(","),
    "allow_methods": ["*"],
    "allow_headers": ["*"],
    "expose_headers": []
}

# パフォーマンスログミドルウェア
class AccessLogMiddleware(BaseHTTPMiddleware):
    """アクセスログ出力ミドルウェア
    アクセス情報をログ出力するミドルウェア
    """

    async def dispatch(
            self,
            request: Request,
            call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:

        # リクエストの処理時間を計測
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        # アクセス情報をログ出力
        access_log.info(
            "",
            extra={
                "process_time": process_time,
                "client_addr": request.client.host,
                "method": request.method,
                "path": request.url.path,
                "query": request.query_params,
                "status_code": response.status_code
            }
        )

        return response

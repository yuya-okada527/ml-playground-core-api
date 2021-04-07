"""キャッシュAPIルーターモジュール

API内で利用しているキャッシュを制御するためのルーター定義を記述するモジュール

TODO
- キャッシュ無効化対象を指定できるようにする
"""

from typing import Dict

from entrypoints.v1.movie.messages.movie_messages import \
    InvalidateCacheResponse
from fastapi import APIRouter
from service.cache_service import exec_invalidate_cache_service

# ルーター作成
router = APIRouter(
    prefix="/v1/cache",
    tags=["cache"],
    # TODO 共通レスポンス
    responses={}
)

@router.post(
    "/invalidate",
    summary="キャッシュ無効化API",
    description="APIで利用しているキャッシュを無効化するAPI",
    response_model=InvalidateCacheResponse,
    response_description="全類似映画判定モデルリスト"
)
async def invalidate_cache() -> InvalidateCacheResponse:

    # サービス実行
    target_cache = exec_invalidate_cache_service()
    print("Executed")
    return InvalidateCacheResponse(
        invalidated=True,
        target_cache=target_cache
    )

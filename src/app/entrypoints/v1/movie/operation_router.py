"""運用APIルーターモジュール

運用で使用するAPIのルーター定義を記述するモジュール
"""
from typing import Dict

from fastapi import APIRouter

HEALTH_CHECK_PATH = "/"

# ルーター作成
router = APIRouter(
    # TODO 暫定対応: GKEのIngressがルートでヘルスチェックしてくるため
    prefix="",
    tags=["operation"],
    # TODO 共通レスポンス
    responses={}
)


@router.get(
    HEALTH_CHECK_PATH,
    summary="ヘルスチェック",
    description="ヘルスチェック機能を提供するAPI."
)
async def ping() -> Dict[str, str]:
    return {
        "health": "ok"
    }

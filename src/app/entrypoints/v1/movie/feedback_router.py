"""ユーザフィードバックAPIルーターモジュール

ユーザフィードバックAPIのルーター定義を記述するモジュール
"""
from entrypoints.v1.movie.messages.movie_messages import LikeSimilarMovie
from fastapi import APIRouter
from service.feedback_service import exec_like_similar_movie_service

# ルーター作成
router = APIRouter(
    prefix="/v1/user/feedback",
    tags=["feedback"],
    # TODO 共通レスポンス
    responses={}
)


@router.post(
    "/like/similar/movie",
    summary="いいね登録API",
    description="ユーザのいいね情報を登録するためのAPI.",
    response_model=LikeSimilarMovie,
    response_description="登録結果"
)
async def like_similar_movie(like: LikeSimilarMovie) -> LikeSimilarMovie:

    # サービス実行
    exec_like_similar_movie_service(
        movie_id=like.movie_id,
        model_type=like.model_type,
        like=like.like
    )

    return like

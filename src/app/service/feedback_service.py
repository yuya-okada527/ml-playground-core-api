"""ユーザフィードバックサービスモジュール

ユーザのフィードバックに関するサービス関数を記述するモジュール
"""
import json

from core.logger import JSON_LOGGER
from domain.enums.similarity_enums import SimilarityModelType


def exec_like_similar_movie_service(
    movie_id: int,
    model_type: SimilarityModelType,
    like: bool
) -> None:

    # ログ経由で、フィードバックを分析できるようにする
    JSON_LOGGER.info(
        json.dumps({
            "movie_id": movie_id,
            "model_type": model_type.value,
            "like": int(like)
        }),
        extra={
            "type": "UserFeedbackLikeSimilarMovie"
        }
    )

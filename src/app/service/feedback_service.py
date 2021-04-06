"""ユーザフィードバックサービスモジュール

ユーザのフィードバックに関するサービス関数を記述するモジュール
"""
import json

from core.logger import create_feedback_logger
from domain.enums.similarity_enums import SimilarityModelType

feedback_log = create_feedback_logger()


def exec_like_similar_movie_service(
    movie_id: int,
    model_type: SimilarityModelType,
    like: bool
) -> None:

    # ログ経由で、フィードバックを分析できるようにする
    feedback_log.info(
        json.dumps({
            "movie_id": movie_id,
            "model_type": model_type.value,
            "like": int(like)
        }),
        extra={
            "feedback_type": "UserFeedbackLikeSimilarMovie"
        }
    )

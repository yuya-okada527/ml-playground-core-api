"""ユーザフィードバックサービスモジュール

ユーザのフィードバックに関するサービス関数を記述するモジュール
"""
from domain.enums.similarity_enums import SimilarityModelType


def exec_like_similar_movie_service(
    movie_id: int,
    model_type: SimilarityModelType,
    like: bool
) -> None:
    # TODO ログ出力
    pass

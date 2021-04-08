from typing import List

from domain.enums.similarity_enums import SimilarityModelType
from pydantic import BaseModel


class MovieSimilarityModelScore(BaseModel):
    """

    Attributes:
        name: モデル名
        total_view: フロントの画面表示に使用した通算回数
        like_count: ユーザからいいねのフィードバックを得られた回数
    """
    name: SimilarityModelType
    total_view: int
    like_count: int


class MovieSimilarityModelMetadata(BaseModel):
    """類似映画判定モデルのメタデータ"""
    best_model: SimilarityModelType
    models: List[MovieSimilarityModelScore]

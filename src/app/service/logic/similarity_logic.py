"""類似性データロジックモジュール

類似性データに関するロジックを記述するモジュール
"""

from functools import lru_cache
from typing import List

from core.logger import create_app_logger
from domain.enums.similarity_enums import SimilarityModelType
from domain.models.metadata.similarity_model import \
    MovieSimilarityModelMetadata
from entrypoints.v1.movie.messages.movie_messages import (MovieResponse,
                                                          SimilarMovieResponse)
from infra.client.solr.solr_api import AbstractSolrClient
from infra.repository.file_repository import AbstractFileRepository
from service.logic.movie_logic import build_search_by_id_query, map_movie

SIMILARITY_MODEL_METADATA = "similarity_models.json"

log = create_app_logger(__file__)


def fetch_similar_movies(
    movie_ids: List[int],
    solr_client: AbstractSolrClient
) -> List[MovieResponse]:
    """類似映画データを取得する

    Args:
        movie_ids (list[int]): 映画IDリスト
        solr_client (AbstractSolrClient): Solrクライアント

    Returns:
        List[MovieResponse]: 映画レスポンスリスト
    """

    # 類似映画を取得
    similar_movie_list = []
    for similar_id in movie_ids:

        # クエリを作成
        movie_id_query = build_search_by_id_query(movie_id=similar_id)

        # 検索結果を取得
        search_result = solr_client.search_movies(movie_id_query)

        # 取得件数を確認
        if len(search_result.response.docs) != 1:
            continue

        # 内部モデルに変換
        similar_movie_list.append(map_movie(search_result.response.docs[0]))

    return similar_movie_list


def map_similar_movies_response(
    movie_id: int,
    model_type: SimilarityModelType,
    similar_movie_list: List[MovieResponse]
) -> SimilarMovieResponse:
    """類似映画レスポンスをマッピングします.

    Args:
        movie_id (int): 映画ID
        model_type (SimilarityModelType): 類似映画判定モデルタイプ
        similar_movie_list (List[MovieResponse]): 類似映画リスト

    Returns:
        SimilarMovieResponse: 類似映画レスポンス
    """
    return SimilarMovieResponse(
        target_id=movie_id,
        model_type=model_type,
        results=similar_movie_list
    )


@lru_cache(maxsize=1)
def get_similarity_model_metadata(
    file_repository: AbstractFileRepository
) -> MovieSimilarityModelMetadata:

    # キャッシュが有効化できているか確認用にデバッグログを出しておく
    log.debug("get_similarity_model_metadata is executed")

    # 類似映画判定モデルのメタデータを取得
    metadata = file_repository.read_json(key=SIMILARITY_MODEL_METADATA)

    return MovieSimilarityModelMetadata(**metadata)

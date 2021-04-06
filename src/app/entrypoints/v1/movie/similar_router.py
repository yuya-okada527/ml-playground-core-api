"""類似映画APIルーターモジュール

類似映画APIのルーター定義を記述するモジュール
"""
from domain.enums.similarity_enums import SimilarityModelType
from entrypoints.v1.movie.messages.movie_messages import (
    AllSimilarityModelsResponse, SimilarMovieResponse)
from fastapi import APIRouter, Depends, Path, Query
from infra.client.solr.solr_api import AbstractSolrClient, get_solr_client
from infra.repository.file_repository import (AbstractFileRepository,
                                              get_file_repository)
from infra.repository.kvs_repository import (AbstractKvsRepository,
                                             get_kvs_repository)
from service.similarity_service import (exec_get_all_similarity_models_service,
                                        exec_search_similar_service)

# ルーター作成
router = APIRouter(
    prefix="/v1/movie/similar",
    tags=["similar"],
    # TODO 共通レスポンス
    responses={}
)


@router.get(
    "/{movie_id}",
    summary="類似映画取得API",
    description="類似映画情報を提供するAPI.",
    response_model=SimilarMovieResponse,
    response_description="類似映画結果"
)
async def search_similar(
    movie_id: int = Path(
        ...,
        ge=0,
        title="映画ID",
        description="指定映画と類似した映画情報を返します."
    ),
    model_type: SimilarityModelType = Query(
        ...,
        title="類似性判定モデルタイプ",
        description="類似性判定に使用するモデルのタイプ"
    ),
    kvs_repository: AbstractKvsRepository = Depends(get_kvs_repository),
    solr_client: AbstractSolrClient = Depends(get_solr_client)
) -> SimilarMovieResponse:

    # サービス実行
    return exec_search_similar_service(
        movie_id=movie_id,
        model_type=model_type,
        kvs_repository=kvs_repository,
        solr_client=solr_client
    )


@router.get(
    "/model/all",
    summary="類似映画判定モデル取得API",
    description="全類似映画判定モデルを取得するAPI",
    response_model=AllSimilarityModelsResponse,
    response_description="全類似映画判定モデルリスト"
)
async def get_all_similarity_models(
    file_repository: AbstractFileRepository = Depends(get_file_repository)
) -> AllSimilarityModelsResponse:
    # サービス実行
    return exec_get_all_similarity_models_service(
        file_repository=file_repository
    )

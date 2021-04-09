from domain.enums.similarity_enums import SimilarityModelType
from domain.models.metadata.similarity_model import (
    MovieSimilarityModelMetadata, MovieSimilarityModelScore)
from service.logic.similarity_logic import select_best_model


def test_select_best_model_call_many_times():

    # テストデータを作成
    metadata = MovieSimilarityModelMetadata(
        best_model=SimilarityModelType.TMDB_SIM,
        models=[
            MovieSimilarityModelScore(
                name=SimilarityModelType.TMDB_SIM,
                total_view=0,
                like_count=0
            ),
            MovieSimilarityModelScore(
                name=SimilarityModelType.GLOVE_SIM,
                total_view=0,
                like_count=0
            )
        ]
    )

    for _ in range(1000):
        select_best_model(metadata)

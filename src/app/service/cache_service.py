

from typing import List

from service.logic.similarity_logic import get_similarity_model_metadata

CACHED_FUNC = {
    "get_similarity_model_metadata": get_similarity_model_metadata
}


def exec_invalidate_cache_service() -> List[str]:

    # 対象のキャッシュを全て削除
    target_cache = []
    for name, func in CACHED_FUNC.items():
        target_cache.append(name)
        func.cache_clear()
    return target_cache

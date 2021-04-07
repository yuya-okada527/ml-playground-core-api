

from typing import List

from service.logic.similarity_logic import get_best_model, get_model_types

CACHED_FUNC = {
    "get_model_types": get_model_types,
    "get_best_model": get_best_model
}


def exec_invalidate_cache_service() -> List[str]:

    # 対象のキャッシュを全て削除
    target_cache = []
    for name, func in CACHED_FUNC.items():
        target_cache.append(name)
        func.cache_clear()
    return target_cache

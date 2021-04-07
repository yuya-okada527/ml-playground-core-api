"""ファイルリポジトリモジュール

ファイルに対するアクセス機能を提供するモジュール
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional, Protocol

from core.config import CoreSettings
from domain.enums.core_enums import Environment

RESOURCE_PATH = os.path.join(
    Path(__file__).resolve().parents[3],
    "resources"
)

CORE_SETTINGS = CoreSettings()


class AbstractFileRepository(Protocol):

    def read_json(self, key: str) -> Dict:
        ...


class LocalFileRepository:

    def __init__(self, resource_path: str = RESOURCE_PATH) -> None:
        self.resource_path = resource_path

    def read_json(self, key: str) -> Dict:
        with open(os.path.join(self.resource_path, key), encoding="utf-8") as f:
            return json.loads(f.read())


class GCSFileRepository:

    def __init__(self) -> None:
        pass

    def read_json(self, key: str) -> Dict:
        # TODO 実装
        return {}


# -------------------------------
# ファイルリポジトリSingleton
# -------------------------------
__FILE_REPOSITORY: Optional[AbstractFileRepository] = None


async def get_file_repository() -> AbstractFileRepository:

    # ファイルリポジトリは、グローバル変数でシングルトンとして管理する
    global __FILE_REPOSITORY
    if __FILE_REPOSITORY is not None:
        return __FILE_REPOSITORY

    # ローカル環境では、ローカルファイルリポジトリを使用
    if CORE_SETTINGS.core_api_env == Environment.LOCAL:
        __FILE_REPOSITORY = LocalFileRepository()
        return __FILE_REPOSITORY

    # その他の環境では、GCSファイルリポジトリを使用
    __FILE_REPOSITORY = GCSFileRepository()
    return __FILE_REPOSITORY

"""ファイルリポジトリモジュール

ファイルに対するアクセス機能を提供するモジュール
"""
import base64
import json
import os
from pathlib import Path
from typing import Dict, Optional, Protocol

from core.config import CoreSettings, GCPSettings
from domain.enums.core_enums import Environment
from google.cloud import storage
from google.oauth2 import service_account

RESOURCE_PATH = os.path.join(
    Path(__file__).resolve().parents[3],
    "resources"
)

CORE_SETTINGS = CoreSettings()

GCP_SETTINGS = GCPSettings()


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

    def __init__(
        self,
        core_settings: CoreSettings = CORE_SETTINGS,
        gcp_settings: GCPSettings = GCP_SETTINGS
    ) -> None:
        self._project_id = core_settings.project_id
        self._credentials_json = json.loads(base64.b64decode(
            gcp_settings.core_api_metadata_service_account_credentials
        ))
        self._credentials = service_account.Credentials.from_service_account_info(
            self._credentials_json
        )
        self._client = storage.Client(
            credentials=self._credentials,
            project=self._project_id
        )
        self._bucket = self._client.get_bucket(
            gcp_settings.core_api_metadata_bucket
        )

    def read_json(self, key: str) -> Dict:

        # blobを取得
        blob = self._bucket.blob(key)

        # 文字列でダウンロード
        content = blob.download_as_text()

        return json.loads(content)


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

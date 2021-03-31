# ML Playground API

ML Playground App 用のコア API を提供します。

- API 仕様書: https://yuya-okada.com/docs

## 使用技術

- 言語: Python3.8
- フレームワーク: FastAPI
- サーバ: uvicorn
- ミドルウェア: Apache Solr, Redis
- インフラ: Docker
- テストフレームワーク: pytest
- 静的解析ツール: flake8
- 型チェッカー: mypy
- CI ツール: Github Actions
- 主要ライブラリ
  - requests
  - pydantic
  - redis-py

## 起動方法

```bash
# ローカル起動
$ uvicorn app.main:app --reload
```

# Word Filter

本リポジトリは TDD のお題である「Word Filter」の Python 実装になります。

## 参考

- https://www.slideshare.net/t_wada/tddbc-exercise
- https://image.slidesharecdn.com/tddbcexercise-110919222207-phpapp01/95/tddbc-19-728.jpg?cb=1316471500

## 環境詳細

- Python : 3.9

### 事前準備

- Docker インストール
- VS Code インストール
- VS Code の拡張機能「Remote - Containers」インストール
  - https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers
- 本リポジトリの clone
- `.env` ファイルを空ファイルでプロジェクト直下に作成
  - proxy が必要な環境の場合は以下を追加
    - `http_proxy=http://PROXY_HOST:PROXY_PORT`
    - `https_proxy=http://PROXY_HOST:PROXY_PORT`

### 開発手順

1. VS Code 起動
2. 左下の緑色のアイコンクリック
3. 「Remote-Containersa: Reopen in Container」クリック
4. しばらく待つ
   - 初回の場合コンテナー image の取得や作成が行われる
5. 起動したら開発可能

## ユニットテスト実行

```
pytest
```

＃# 🗃️ InventoryManager（商品管理アプリ）

フロントエンド・バックエンドをシンプルに構築した、在庫管理用のWebアプリです。  
小規模なお店やフリーランスの方向けに、製品の検索・表示・ソートを簡単に行えます。

---

🔗 [デモサイトはこちら](https://inventorymanager-u2gc.onrender.com)

---

## 🛠️ 使用技術

- **バックエンド**: Python / Flask / Flask-SocketIO  
- **フロントエンド**: HTML / CSS   
- **データベース**: SQLite  
- **デプロイ**: Render  
- **Webサーバー**: Gunicorn + Eventlet

---

## 🔍 主な機能

- 商品番号やキーワードによる **検索**
- 商品名・価格・在庫情報の **表示**
- 「価格順」「在庫順」などの **ソート機能**
- Web上で誰でもアクセス可能な **デモサイト**

---

## 🧪 ローカル環境での実行方法

1. リポジトリをクローン  
   ```bash
   git clone https://github.com/alecmcclendon/InventoryManager.git
   cd InventoryManager

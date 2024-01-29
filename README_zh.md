# InterDiD 項目

- [英文版](README.md)

## 技術文檔
這傢伙太懶了，沒有寫文檔，所以只能通過閱讀代碼來了解。

## 演示
https://youtu.be/V_X3ksqzREA

## 架構
- 前端
  - Vue
  - Headbreaker
- 後端
  - Django Rest Framework
  - 數據庫
  - Linebot
- 部署（使用 Docker）
  - 服務器
  - Mariadb
  - Nginx
  - Ngrok (WEBHOOK)

## 功能
- 前端
  - [x] 網頁
  - [x] 拼圖
- 後端
  - [x] API
  - [x] 數據庫
  - [x] Linebot
  - [x] Docker化

## 開始使用
- [僅 Docker 的逐步視頻](https://youtu.be/???)
1. 克隆此存儲庫
2. 將文件 `.env_example` 重命名為 `.env`
3. 用您自己的 api 密鑰和設置填寫 `.env` 文件
4. 如何獲取 LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN
   1. 轉到 [LINE Developer Console](https://developers.line.biz/console/)
   2. 創建一個新的提供者
   3. 創建一個新的頻道
   4. 轉到基本設置選項卡
   5. 將頻道秘密複製到 `.env`
   6. 轉到 Messaging API 選項卡
   7. 將頻道訪問令牌複製到 `.env`
   8. 並將 webhook url 設置為 `https://<your_domain>/api/linebot`

### 不使用 Docker 部署 [僅 WebHook]
1. 轉到 [NGROK](https://ngrok.com/) 下載並設置 Ngrok。
   1. 註冊一個免費帳戶
   2. 下載 ngrok 客戶端
   3. 創建一個域
   4. 創建一個邊緣，然後轉到 Request Headers 並粘貼名稱：`ngrok-skip-browser-warning` 值：`69420`
   5. 點擊開始隧道並從命令行開始。
2. 轉到 `.env` 並將 APP_HOST 設置為 `https://<your_domain>`。
3. 轉到 [LINE Developer Console](https://developers.line.biz/console/) 並將 webhook url 設置為 `https://<your_domain>/api/linebot`。
4. 運行 `ngrok http 8000` 以啟動 ngrok 服務器。
5. 運行 `python manage.py runserver 0.0.0.0:8000` 以啟動服務器。

### 使用 Docker 部署 [Webhook]
1. 轉到 [NGROK](https://ngrok.com/) 下載並設置 Ngrok。
   1. 註冊一個免費帳戶
   2. 下載 ngrok 客戶端
   3. 創建一個域
   4. 創建一個邊緣，然後轉到 Request Headers 並粘貼名稱：`ngrok-skip-browser-warning` 值：`69420`
   5. 點擊開始隧道並從 docker 開始。
2. 用您自己的 `NGROK_AUTHTOKEN`，`NGROK_EDGE` 和 `APP_HOST` 填寫 `.env` 文件。
3. 轉到 [LINE Developer Console](https://developers.line.biz/console/) 並將 webhook url 設置為 `https://<your_domain>/api/linebot`。
4. 運行 `docker-compose up -d --build` 以啟動服務器。

### 使用 Docker 部署 [無 Webhook]
1. 轉到 `docker-compose.yml` 並刪除 ngrok 服務。
2. 在根目錄中創建一個名為 `ssl` 的文件夾，並將您自己的 ssl 證書和密鑰放入其中。
3. 轉到 `nginx.conf` 並更改 ssl 證書，密鑰路徑和域名。
4. 轉到 `.env` 並將 APP_HOST 設置為 `https://<your_domain>`。
5. 運行 `docker-compose up -d --build` 以啟動服務器。

### 自定義端口（如果需要，默認服務器 = 8000，db = 3306，nginx = 80, 443，ngrok = 4040）
* 轉到 `docker-compose.yml` 並將服務（web，db，nginx，ngrok）端口號更改為您自己的
* 轉到 `Dockerfile` 並更改導出端口號
* 轉到 `nginx.conf` 並更改端口號
* 轉到 `entrypoint.sh` 並更改端口號

## 活動
![Alt](https://repobeats.axiom.co/api/embed/7a2e89f748c1cc8887da9f8b62a1a673c0710e10.svg "Repobeats 分析圖像")
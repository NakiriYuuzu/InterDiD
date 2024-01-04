# InterDiD 項目

- [英文版](README.md)

## 技術文檔
這傢伙太懶了，沒有寫文檔，所以只能通過閱讀代碼來了解。

## 演示


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

## 入門指南
* 克隆這個存儲庫
* 將 `.env_example` 文件重命名爲 `.env`
* 在 `.env` 文件中填寫你自己的 api 密鑰和設置
* 如何獲取 LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN
  * 轉到 [LINE 開發者控制台](https://developers.line.biz/console/)
  * 創建一個新的提供者
  * 創建一個新的頻道
  * 轉到基本設置選項卡
  * 將 Channel secret 複製到 `.env`
  * 轉到消息 API 選項卡
  * 將 Channel access token 複製到 `.env`

### 自定義端口（如果需要，默認服務器 = 8000, 數據庫 = 3306, ngrok = 4040, nginx = 80, 443）
* 轉到 `docker-compose.yml` 並更改服務（web, db, nginx）的端口號爲您自己的
* 轉到 `Dockerfile` 並更改導出端口號
* 轉到 `nginx.conf` 並更改端口號
* 轉到 `entrypoint.sh` 並更改端口號

### 使用 Webhook
- 轉到 `docker-compose.yml` 並刪除 nginx 服務。
- 轉到 [NGROK](https://ngrok.com/) 並下載 ngrok。
- 運行 `./ngrok http 8000` 啓動 ngrok 服務器。
- 轉到 `.env` 並將 APP_HOST 設置爲 `https://<your_domain>`

### 不使用 Webhook（使用自己的域名和 ssl）
- 轉到 `docker-compose.yml` 並刪除 ngrok 服務。
- 在根目錄下創建一個 `ssl` 文件夾，並將你自己的 ssl 證書和密鑰放進去。
- 轉到 `nginx.conf` 並更改 ssl 證書和密鑰路徑。
- 轉到 `nginx.conf` 並更改域名。
- 轉到 `.env` 並將 APP_HOST 設置爲 `https://<your_domain>`

### 使用 Docker 部署
* 運行 `docker-compose up -d --build` 啓動服務器
* 轉到 [LINE 開發者控制台](https://developers.line.biz/console/) 並設置 webhook url 爲 `https://<your_domain>/api/linebot`

## 活動
![Alt](https://repobeats.axiom.co/api/embed/7a2e89f748c1cc8887da9f8b62a1a673c0710e10.svg "Repobeats 分析圖像")
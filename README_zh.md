# InterDiD 項目

- [English](README.md)

## 演示
- [設置服務器](https://www.youtube.com/watch?v=M37pfq72HPY&ab_channel=%E3%82%86%E3%81%9A)
- [演示視頻](https://youtu.be/V_X3ksqzREA)

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
1. 克隆此存儲庫
2. 將文件 `.env_example` 重命名為 `.env`
3. 用您自己的 api 密鑰和設置填寫 `.env` 文件
4. 如何獲取 LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN
   1. 轉到 [LINE Developer Console](https://developers.line.biz/console/)
   2. 創建一個新的提供者
   3. 創建一個新的頻道
   4. 選擇 message api
   5. 將頻道秘密複製到 `.env`
   6. 轉到 Messaging API 選項卡
   7. 將頻道訪問令牌複製到 `.env`
5. 如果使用 Ngrok，轉到 [NGROK](https://ngrok.com/) 下載並設置 Ngrok。
   1. 註冊一個免費帳戶
   2. 下載 ngrok 客戶端 (使用Docker則跳過)
   3. 創建一個域
   4. 創建一個邊緣，然後轉到 Request Headers 並粘貼名稱：`ngrok-skip-browser-warning` 值：`69420`
   5. 點擊開始隧道並從命令行開始。
6. 轉到 [LINE Developer Console](https://developers.line.biz/console/) 並將 webhook url 設置為 `https://<your_domain>/api/linebot`。
7. 如果使用 Docker：
   1. （如果已安裝則跳過）運行 `chmod +x install_docker.sh` 和 `./install_docker.sh` 以安裝 docker 和 docker-compose。
   2. 運行 `docker-compose up -d --build` 以啟動服務器。
8. 如果不使用 Docker：
   1. 使用您自己的域名，並將 `.env` 和 `Line Developer Console` 中的 `APP_HOST` 替換為它。
   2. 運行從 ngrok 複製的命令。
   3. 運行 `python manage.py runserver 0.0.0.0:8000` 以啟動服務器。
9. 轉到 `https://<your_domain>/admin` 並使用 `.env` 文件中的用戶名和密碼登錄。
10. 轉到 `https://<your_domain>/admin/puzzle` 創建難度並設置難度。

### 自定義端口（如果需要，默認服務器 = 8000，db = 3306，nginx = 80, 443，ngrok = 4040）
* 轉到 `docker-compose.yml` 並將服務（web，db，nginx，ngrok）端口號更改為您自己的
* 轉到 `Dockerfile` 並更改導出端口號
* 轉到 `nginx.conf` 並更改端口號
* 轉到 `entrypoint.sh` 並更改端口號

### Line Beacon 設置
1. 轉到 [LINE Developer Beacon](https://manager.line.biz/beacon/register)。
2. 點擊 `Line Simple Beacon` 按鈕。
3. 選擇您創建的 Linebot。
4. 點擊 `Hardware ID` 按鈕。
5. 複製 `Hardware ID` 並轉到 `https://<your_domain>/admin/beacon/` 創建一個新的 beacon。

## 活動
![Alt](https://repobeats.axiom.co/api/embed/7a2e89f748c1cc8887da9f8b62a1a673c0710e10.svg "Repobeats 分析圖像")
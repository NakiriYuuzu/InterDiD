# 使用 Python 官方映像作爲基礎
FROM python:3.9

# 設置工作目錄
WORKDIR /app

# 將依賴文件複製到容器中
COPY requirements.txt ./

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製項目文件到容器中
COPY . .

# 複製並設置 entrypoint.sh 執行權限
COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# 暴露端口
EXPOSE 8000

# 設置容器入口點
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

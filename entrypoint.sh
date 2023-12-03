#!/bin/bash

# 5，直到數據庫服務啟動
for i in {1..5}
do
  echo "Waiting for database service $i seconds"
  sleep 1
done

# 執行數據庫遷移
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

# 執行文件遷移
echo "Apply static files migrations"
python manage.py collectstatic --noinput

# 创建超级用户
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${USER_ACCOUNT}', 'admin@example.com', '${USER_PASSWORD}') if not User.objects.filter(username='${USER_ACCOUNT}').exists() else None" | python manage.py shell

# 執行測試
echo "Running tests"
python manage.py test

# 啟動 Django 服務
echo "Starting Django service"
exec python manage.py runserver 0.0.0.0:8000
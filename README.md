# InterDiD Project

- [中文](README_zh.md)

## demo
- [setup line](https://youtu.be/???)
- [setup ngrok](https://youtu.be/???)
- [setup server](https://youtu.be/???)
- [demo video](https://youtu.be/V_X3ksqzREA)


## Architecture
- Frontend
  - Vue
  - Headbreaker
- Backend
  - Django Rest Framework
  - Database
  - Linebot
- Deployment (Docker)
  - Server
  - Mariadb
  - Nginx
  - Ngrok (WEBHOOK)

## Features
- Frontend
  - [x] Web
  - [x] puzzle
- backend
  - [x] API
  - [x] Database
  - [x] Linebot
  - [x] Dockerized

## Getting Started
1. Clone this repository
2. Rename the file `.env_example` to `.env`
3. Fill in the `.env` file with your own api key and settings
4. How to get LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN 
   1. go to [LINE Developer Console](https://developers.line.biz/console/)
   2. create a new provider
   3. create a new channel
   4. go to Basic settings tab
   5. copy the Channel secret to `.env`
   6. go to Messaging API tab
   7. copy the Channel access token to `.env`
   8. and set webhook url to `https://<your_domain>/api/linebot`
5. If using docker, run `chmod +x install_docker.sh` and `./install_docker.sh` to install docker and docker-compose.
6. Follow the steps below to deploy.

### Deploy without Docker [Only WebHook]
1. Go to [NGROK](https://ngrok.com/) download and setup Ngrok.
   1. Sign up for a free account
   2. Download the ngrok client
   3. Create a domain
   4. Create an edge, after go to Request Headers and paste name: `ngrok-skip-browser-warning` value: `69420`
   5. Click the start tunel and select start from command line.
2. go to `.env` and set APP_HOST to `https://<your_domain>`.
3. go to [LINE Developer Console](https://developers.line.biz/console/) and set webhook url to `https://<your_domain>/api/linebot`.
4. run `ngrok http 8000` to start the ngrok server.
5. run `python manage.py runserver 0.0.0.0:8000` to start the server.

### Deploy with Docker [Webhook]
1. Go to [NGROK](https://ngrok.com/) download and setup Ngrok.
   1. Sign up for a free account
   2. Download the ngrok client
   3. Create a domain
   4. Create an edge, after go to Request Headers and paste name: `ngrok-skip-browser-warning` value: `69420`
   5. Click the start tunel and select start from docker.
2. Fill in the `.env` file with your own `NGROK_AUTHTOKEN`, `NGROK_EDGE` and `APP_HOST`.
3. go to [LINE Developer Console](https://developers.line.biz/console/) and set webhook url to `https://<your_domain>/api/linebot`.
4. run `docker-compose up -d --build` to start the server.

### Deploy with Docker [Without Webhook]
1. Go to `docker-compose.yml` and delete the ngrok service.
2. Create a folder named `ssl` in the root directory and put your own ssl certificate and key in it.
3. go to `nginx.conf` and change the ssl certificate, key path and the domain name.
4. go to `.env` and set APP_HOST to `https://<your_domain>`.
5. go to [LINE Developer Console](https://developers.line.biz/console/) and set webhook url to `https://<your_domain>/api/linebot`.
6. run `docker-compose up -d --build` to start the server.

### Customize Port (if needed, default server = 8000, db = 3306, nginx = 80, 443,ngrok = 4040)
* go to `docker-compose.yml` and change the service (web, db, nginx, ngrok) port number to your own
* go to `Dockerfile` and change the export port number
* go to `nginx.conf` and change the port number
* go to `entrypoint.sh` and change the port number

## Activity
![Alt](https://repobeats.axiom.co/api/embed/7a2e89f748c1cc8887da9f8b62a1a673c0710e10.svg "Repobeats analytics image")
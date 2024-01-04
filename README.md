# InterDiD Project

- [中文](README_zh.md)

## Documentation
This guy is too lazy to write documentation, so you can only understand it by reading the code.

## Demo


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
* clone this repository
* rename the file `.env_example` to `.env`
* fill in the `.env` file with your own api key and settings
* How to get LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN
  * go to [LINE Developer Console](https://developers.line.biz/console/)
  * create a new provider
  * create a new channel
  * go to Basic settings tab
  * copy the Channel secret to `.env`
  * go to Messaging API tab
  * copy the Channel access token to `.env`

### Customize Port (if needed, default server = 8000, db = 3306, nginx = 80, 443)
* go to `docker-compose.yml` and change the service (web, db, nginx) port number to your own
* go to `Dockerfile` and change the export port number
* go to `nginx.conf` and change the port number
* go to `entrypoint.sh` and change the port number

### With Webhook
- go to `docker-compose.yml` and remove the nginx service.
- go to [NGROK](https://ngrok.com/) and download the ngrok.
- run `./ngrok http 8000` to start the ngrok server.
- go to `.env` and set APP_HOST to `https://<your_domain>`

### Without Webhook (use own domain and ssl)
- go to `docker-compose.yml` and remove the ngrok service.
- create a `ssl` folder in root and put your own ssl certificate and key in it.
- go to `nginx.conf` and change the ssl certificate and key path.
- go to `nginx.conf` and change the domain name.
- go to `.env` and set APP_HOST to `https://<your_domain>`

### Deploy with Docker
* run `docker-compose up -d --build` to start the server
* go to [LINE Developer Console](https://developers.line.biz/console/) and set webhook url to `https://<your_domain>/api/linebot`

## Activity
![Alt](https://repobeats.axiom.co/api/embed/7a2e89f748c1cc8887da9f8b62a1a673c0710e10.svg "Repobeats analytics image")
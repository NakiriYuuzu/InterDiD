# InterDiD Project

- [中文](README_zh.md)

## demo
- [setup server](https://www.youtube.com/watch?v=M37pfq72HPY&ab_channel=%E3%82%86%E3%81%9A)
- [web preview](https://youtu.be/zyp4eNCiXhs)
- [Line App Preview](https://youtu.be/DHHUUk9R9S4)

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
### WARNING 
#### IF WINDOWS Please use this command on git
```bash
git config --global core.autocrlf false
```
1. Clone this repository
2. Rename the file `.env_example` to `.env`
3. Fill in the `.env` file with your own api key and settings
4. How to get LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN 
   1. go to [LINE Developer Console](https://developers.line.biz/console/)
   2. create a new provider
   3. create a new channel
   4. pick the message api
   5. copy the Channel secret to `.env`
   6. go to Messaging API tab
   7. copy the Channel access token to `.env`
5. If using Ngrok, go to [NGROK](https://ngrok.com/) download and setup Ngrok.
   1. Sign up for a free account
   2. Download the ngrok client (skip if using Docker)
   3. Create a domain
   4. Create an edge, after go to Request Headers and paste name: `ngrok-skip-browser-warning` value: `69420`
   5. Click the start tunel and select start from command line and click the copy. 
6. Go to [LINE Developer Console](https://developers.line.biz/console/) and set webhook url to `https://<your_domain>/api/linebot`.
7. For Docker:
   1. (Skip if install) Run `chmod +x install_docker.sh` and `./install_docker.sh` to install docker and docker-compose.
   2. Run `docker-compose up -d --build` to start the server.
8. Without Docker:
   1. Use your own domain name and replace the `APP_HOST` in `.env` and `Line Developer Console` with it.
   2. Run the command copied from ngrok.
   3. Run `python manage.py runserver 0.0.0.0:8000` to start the server.
9. Go to `https://<your_domain>/admin` and login with the username and password in `.env` file.
10. Go to `https://<your_domain>/admin/puzzle` create a difficulty and set the difficulty.

### Customize Port (if needed, default server = 8000, db = 3306, nginx = 80, 443, ngrok = 4040)
* go to `docker-compose.yml` and change the service (web, db, nginx, ngrok) port number to your own
* go to `Dockerfile` and change the export port number
* go to `nginx.conf` and change the port number
* go to `entrypoint.sh` and change the port number

### Line Beacon Setup
1. Go to [LINE Developer Beacon](https://manager.line.biz/beacon/register).
2. Click the `Line Simple Beacon` button.
3. Select the Linebot you created.
4. Click the `Hardware ID` button.
5. Copy the `Hardware ID` and go to `https://<your_domain>/admin/beacon/` and create a new beacon.

## Activity
![Alt](https://repobeats.axiom.co/api/embed/7a2e89f748c1cc8887da9f8b62a1a673c0710e10.svg "Repobeats analytics image")
# InterDiD Project

- [中文](README_zh.md)

## Documentation
this guys so lazy to write documentation, so just read the code

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

### Customize Port (if needed, default server = 8000, db = 3306, ngrok = 4040, nginx = 80, 443)
* go to `docker-compose.yml` and change the service (web, db, ngrok, nginx) port number to your own
* go to `Dockerfile` and change the export port number
* go to `nginx.conf` and change the port number
* go to `ngrok.yml` and change the port number

### With Webhook
- go to `docker-compose.yml` and remove the nginx service.
- go ngrok website and get your own authtoken and replace it in `.env`.
- go to `ngrok.yml` and change the domain and host_header to your own ngrok domain.
- go to `.env` and set APP_HOST to `https://<your_domain>`

### Without Webhook (use own domain and ssl)
- go to `docker-compose.yml` and remove the ngrok service.
- create a `ssl` folder in root and put your own ssl certificate and key in it.
- go to `nginx.conf` and change the ssl certificate and key path.
- go to `nginx.conf` and change the domain name.
- go to `.env` and set APP_HOST to `https://<your_domain>`

### Deploy with Docker
* run `docker-compose up -d --build` to start the server
* go to line developer console and set webhook url to `https://<your_domain>/api/linebot`

## Activity
![Alt](https://repobeats.axiom.co/api/embed/7a2e89f748c1cc8887da9f8b62a1a673c0710e10.svg "Repobeats analytics image")
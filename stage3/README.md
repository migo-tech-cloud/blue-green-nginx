# Stage 2: Blue/Green with Nginx Upstreams

# Blue-Green Deployment with Nginx and Docker Compose

This project demonstrates a **Blue-Green Deployment** setup using **Nginx** as a reverse proxy and two backend application pools (`blue` and `green`).  
It ensures zero downtime when deploying new versions.

---

## 🛠️ Prerequisites

- Docker and Docker Compose installed  
- Git installed  
- (For EC2) Ubuntu instance with ports **8080**, **8081**, **8082** open in the Security Group  
- An `.env` file configured (see `.env.example`)

---

## 📥 Clone the Repository

git clone https://github.com/<your-username>/blue-green-nginx.git
cd blue-green-nginx

---

## ⚙️ Configure Environment Variables
Create a .env file based on .env.example:
cp .env.example .env

Then edit it:
nano .env

Example:
BLUE_IMAGE=
GREEN_IMAGE=
ACTIVE_POOL=blue
RELEASE_ID_BLUE=blue-v1
RELEASE_ID_GREEN=green-v1
PORT=3000

---

## 🚀 Run Locally

sudo docker compose up -d

Then visit:

http://localhost:8080/version → Nginx reverse proxy

http://localhost:8081/version → Blue app

http://localhost:8082/version → Green app

---

## ☁️ Deploy on AWS EC2

SSH into your EC2 instance:
ssh -i "your-key.pem" ubuntu@<EC2-PUBLIC-IP> **OR** connect via AWS terminal **OR** via MobaXterm

Install Docker:
sudo apt update
sudo apt install docker.io docker-compose-plugin -y
sudo systemctl enable docker && sudo systemctl start docker

Clone this repo and start the stack:
git clone https://github.com/<your-username>/blue-green-nginx.git
cd blue-green-nginx
sudo docker compose up -d

Then visit:
http://<EC2-PUBLIC-IP>:8080/version

---

## 🔄 Switching Between Blue and Green

To switch pools, edit .env:
ACTIVE_POOL=green

Then restart Nginx:
sudo docker compose restart nginx
Now Nginx routes traffic to the green container.

---

## 🧹 Teardown
To stop and remove containers:
sudo docker compose down

---

## 🧠 Notes

Nginx dynamically reads which pool (blue or green) to serve using environment variables.

The entrypoint.sh script rewrites the active target in the Nginx config at container startup.

This structure allows deploying a new version to the idle pool, testing it, then switching with zero downtime.

---

## Stage 3 – Observability & Alerts

### Setup

1. Copy `.env.example` → `.env`
2. Add your `SLACK_WEBHOOK_URL` from Slack (Incoming Webhook).
3. Run:
   ```bash
   docker compose up --build -d

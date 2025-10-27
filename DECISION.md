# DECISION.md

## Overview
This document explains the reasoning behind key architectural and configuration choices in this Blue-Green deployment setup.

---

### 1. Nginx as Reverse Proxy
Nginx was chosen for its simplicity, speed, and flexibility. It sits in front of both app versions and routes traffic based on an environment variable (`ACTIVE_POOL`).

---

### 2. Blue-Green Structure
Two identical app containers (`blue` and `green`) allow deploying updates safely:
- Users continue using the active pool.
- The inactive pool is updated and tested.
- Once validated, we switch traffic instantly.

---

### 3. Docker Compose
Docker Compose simplifies multi-container management.  
We use environment variables for dynamic configuration and container linking.

---

### 4. EC2 Deployment
Ubuntu EC2 is used for cloud testing. It provides an environment similar to production, with control over networking and firewall rules.

---

### 5. Future Enhancements
- Automate blue-green switch with CI/CD (GitHub Actions or Jenkins).
- Add health checks before switching pools.
- Use AWS Elastic IP to maintain a stable public endpoint.

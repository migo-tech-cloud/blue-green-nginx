# Stage 2: Blue/Green with Nginx Upstreams

## How It Works
This setup runs two Node.js apps (Blue and Green) behind an Nginx proxy.
Nginx sends traffic to Blue by default and switches to Green automatically if Blue fails.

### Endpoints
- Public entrypoint (via Nginx): `http://localhost:8080`
- Direct Blue: `http://localhost:8081`
- Direct Green: `http://localhost:8082`

---

## 🧩 Setup

1. Copy `.env.example` → `.env` and fill in:
   - BLUE_IMAGE, GREEN_IMAGE, RELEASE_IDs
   - ACTIVE_POOL=blue
   - PORT=3000

2. Run the containers:
   ```bash
   docker compose up -d

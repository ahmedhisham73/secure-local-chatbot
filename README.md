# 🧠 Secure Local Chatbot Architecture – Technical Documentation

> **Purpose**: Provide a fully containerized, JWT-secured, self-hosted chatbot architecture using `llama-cpp`, reverse-proxied via `NGINX` with HTTPS. Built for high-compliance, isolated enterprise environments.

---

## 📁 Project Directory Structure

```
chatbot_enterprise_local/
├── docker-compose.yml
├── nginx/
│   ├── nginx.conf
│   └── certs/
├── app/
│   ├── auth_service/
│   │   ├── main.py
│   │   ├── ldap_sim.py
│   │   ├── requirements.txt
│   ├── chat_service/
│   │   ├── main.py
│   │   ├── inference.py
│   │   ├── requirements.txt
│   ├── shared/
│   │   ├── jwt_utils.py
│   │   ├── rbac.py
│   ├── log_service/
│   │   └── responses_logs/
│   │       └── chatbot_logs.log
│   ├── frontend/
│   │   ├── src/
│   │   ├── public/
│   │   ├── index.html
│   │   ├── vite.config.js
│   │   ├── package.json
├── models/
│   └── TinyLLAMA/
│       └── tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf  ❌ Not included in repo
├── data/
│   └── users/
│       └── users.yaml
```



---

## 🔐 Auth Service
- Runs on: `http://localhost:5000`
- Handles login
- Verifies credentials via `users.yaml`
- Generates JWT token using `jwt_utils.py`

### 🔓 Endpoint:
- `POST /login` → returns token + user info

### ✅ JWT Payload:
```json
{
  "username": "analyst1",
  "role": "analyst",
  "exp": <timestamp>
}
```

---

## 🤖 Chat Service
- Runs on: `http://localhost:5101`
- Validates JWT tokens using decorators
- Generates LLM response using `llama-cpp-python`
- Logs every request/response with log rotation

### Endpoint:
- `POST /chat` → accepts prompt & returns model response

### ENV:
- `MODEL_PATH=/app/models/TinyLLAMA/tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf`
- `LOG_DIR=/app/log_service/responses_logs`

---

## 💻 Frontend (React + Vite + TailwindCSS)
- Path: `app/frontend/`
- Handles login and chat
- Clean and modern UI

### Commands:
```bash
cd app/frontend
npm install
npm run dev
```

- Exposed on: `https://localhost:5173`
- Communicates with backend via NGINX reverse proxy

---

## 🌐 NGINX (HTTPS Reverse Proxy)
- Path: `nginx/nginx.conf`
- Runs on: `https://localhost:8443`
- Proxies `/login` to `auth_service`, `/chat` to `chat_service`
- Supports CORS and TLS with self-signed certs

---

## 🐳 Docker Compose
```yaml
version: '3.8'
services:
  auth_service:
    build: ./app/auth_service
    ports: ["5000:5000"]
    volumes:
      - ./data/users:/app/data/users
      - ./app/shared:/app/shared
    environment:
      - JWT_SECRET_KEY=your_secret_key
    networks: [chatbot_network]

  chat_service:
    build: ./app/chat_service
    ports: ["5101:5101"]
    depends_on: [auth_service]
    volumes:
      - ./app/shared:/app/shared
      - ./app/chat_service/models/TinyLLAMA:/app/models/TinyLLAMA
      - ./app/log_service/responses_logs:/app/log_service/responses_logs
    environment:
      - MODEL_PATH=/app/models/TinyLLAMA/tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf
      - LOG_DIR=/app/log_service/responses_logs
    networks: [chatbot_network]

  nginx:
    image: nginx:latest
    ports: ["8080:80", "8443:443"]
    depends_on: [auth_service, chat_service]
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    networks: [chatbot_network]

networks:
  chatbot_network:
    driver: bridge
```

---

## 🔐 Security Summary
- JWT with role-based access control
- HTTPS via NGINX self-signed certs
- Logging via `loguru` with rotation and compression
- Clean directory structure
- Services isolated in Docker containers

---

## 🧪 Curl Test
```bash
# Login
curl -k https://localhost:8443/login -H "Content-Type: application/json" -d '{"username": "analyst1", "password": "pass123"}'

# Chat
curl -k https://localhost:8443/chat -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d '{"prompt": "What are the key banking risks in Egypt?"}'
```

---

## 🔮 Roadmap
- ✅ NGINX reverse proxy & TLS
- ✅ Role-based access (RBAC)
- ✅ React frontend
- 🔜 Token refresh flow
- 🔜 Admin panel for role mgmt
- 🔜 CI/CD for GitHub deployment

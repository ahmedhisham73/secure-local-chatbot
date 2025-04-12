## 🧠 Secure Local Chatbot Architecture - Documentation (Updated)

## 📁 Project Structure
```
chatbot_enterprise_local/
├── docker-compose.yml
├── nginx/
│   ├── nginx.conf
│   └── certs/                  # Self-signed certs (if using HTTPS)
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
├── models/
│   └── TinyLLAMA/
│       └── tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf
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
- Exposed endpoint:
  - `POST /login` → returns token + user info

### ✅ JWT Payload
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
- Requires valid JWT token (checked via `rbac.py`)
- Generates LLM response using `llama-cpp-python`
- Logs each request/response
- Model file loaded from volume mount

### Exposed endpoint:
- `POST /chat` → returns response based on prompt

### Environment Variables
- `MODEL_PATH=/app/models/TinyLLAMA/tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf`
- `LOG_DIR=/app/log_service/responses_logs`

---

## 🌐 NGINX (Reverse Proxy with HTTPS)
- Runs on: `https://localhost:8443`
- Proxies:
  - `/login` → auth_service
  - `/chat` → chat_service
- Self-signed certs mounted via volume

### 🔐 TLS Enabled Reverse Proxy
```
https://localhost:8443/login
https://localhost:8443/chat
```

---

## 🐳 Docker Compose
```yaml
version: '3.8'

services:
  auth_service:
    build: ./app/auth_service
    ports:
      - "5000:5000"
    environment:
      - JWT_SECRET_KEY=your_secret_key
    volumes:
      - ./data/users:/app/data/users
      - ./app/shared:/app/shared
    networks:
      - chatbot_network

  chat_service:
    build: ./app/chat_service
    ports:
      - "5101:5101"
    depends_on:
      - auth_service
    environment:
      - MODEL_PATH=/app/models/TinyLLAMA/tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf
      - LOG_DIR=/app/log_service/responses_logs
    volumes:
      - ./app/shared:/app/shared
      - ./app/chat_service/models/TinyLLAMA:/app/models/TinyLLAMA
      - ./app/log_service/responses_logs:/app/log_service/responses_logs
    networks:
      - chatbot_network

  nginx:
    image: nginx:latest
    ports:
      - "8080:80"
      - "8443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    depends_on:
      - auth_service
      - chat_service
    networks:
      - chatbot_network

networks:
  chatbot_network:
    driver: bridge
```

---

## 🧪 Curl Test
### Login:
```bash
curl -k https://localhost:8443/login \
  -H "Content-Type: application/json" \
  -d '{"username": "analyst1", "password": "pass123"}'
```

### Chat:
```bash
curl -k https://localhost:8443/chat \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the key banking risks in Egypt?"}'
```

---

## 🛡 Security Summary
- JWT-based Auth with Expiration
- RBAC decorators: `@requires_auth`, `@requires_role`
- HTTPS termination via NGINX
- Services isolated in Docker containers
- Logging with rotation & compression using `loguru`

---

## 🔮 Next Improvements
- Add Refresh Token endpoint
- Add User Role Management (admin view)
- Add Prometheus & Grafana for monitoring
- Streamlit/React frontend for usability
- CI/CD GitHub Action for auto-deploy

---

> ✨ Built for secure AI services in enterprise-grade infrastructure 💼



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
├── models/
│   └── TinyLLAMA/
│       └── tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf  ❌ Not included in repo
├── data/
│   └── users/
│       └── users.yaml
```

---

## 🔐 Auth Service

- **Port**: `5000`
- **Responsibilities**:
  - Handles login via `/login`
  - Verifies credentials in YAML (`users.yaml`)
  - Issues JWT token via `jwt_utils.py`

### 🔓 Endpoint

```http
POST /login
```

### ✅ JWT Payload

```json
{
  "username": "analyst1",
  "role": "analyst",
  "exp": 1744474210
}
```

---

## 🤖 Chat Service

- **Port**: `5101`
- **Responsibilities**:
  - Validates JWT via decorators
  - Calls TinyLLAMA via `llama-cpp-python`
  - Logs prompts & responses using `loguru`

### Environment Variables

```
MODEL_PATH=/app/models/TinyLLAMA/tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf
LOG_DIR=/app/log_service/responses_logs
```

---

## 🌐 NGINX Reverse Proxy (HTTPS)

- **Port**: `8443`
- **Features**:
  - TLS termination via self-signed or CA cert
  - CORS preflight support
  - Reverse proxies:
    - `/login` ➜ `auth_service`
    - `/chat` ➜ `chat_service`

---

## 🐳 Docker Compose Setup

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

## 🧪 Curl Testing

### Login Request

```bash
curl -k https://localhost:8443/login \
  -H "Content-Type: application/json" \
  -d '{"username": "analyst1", "password": "pass123"}'
```

### Chat Request

```bash
curl -k https://localhost:8443/chat \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the key banking risks in Egypt?"}'
```

---

## 🔐 Security Design

- 🔒 JWT + Role-based Access Control (`@requires_auth`, `@requires_role`)
- 🔐 TLS-encrypted traffic (via `nginx`)
- 🔐 Explicit CORS control (headers + preflight logic)
- 🔐 Logs rotated, compressed, and persisted
- 🔐 Internal Docker network for service isolation

---

## 🎯 Future Roadmap

- [ ] Refresh Token + Logout endpoint
- [ ] RBAC Admin Panel (React)
- [ ] Monitoring via Prometheus + Grafana
- [ ] Model switching via UI
- [ ] GitHub Actions for CI/CD

---

> ✅ Production-grade LLM deployment architecture  
> 🔐 Designed for regulated environments (banking, fintech, telcos)  
> 👨‍💻 Built by engineers. Not just a pretty demo.

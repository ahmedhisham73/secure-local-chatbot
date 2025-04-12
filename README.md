🧠 Secure Local Chatbot Architecture – Technical Documentation
Purpose: Provide a fully containerized, JWT-secured, self-hosted chatbot architecture using llama-cpp, reverse-proxied via NGINX with HTTPS. Built for high-compliance, isolated enterprise setups.

📁 Project Directory Layout
bash
Copy
Edit
chatbot_enterprise_local/
├── docker-compose.yml
├── nginx/
│   ├── nginx.conf
│   └── certs/                      # TLS certs (self-signed or CA-issued)
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
│   └── TinyLLAMA/                  # 🔒 Excluded from Git
│       └── tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf
├── data/
│   └── users/
│       └── users.yaml
🔐 Auth Service
Port: 5000

Purpose:

Accepts user credentials via /login

Validates against YAML-based LDAP mock (users.yaml)

Returns JWT with username, role, and expiry

Security: Uses HS256 tokens via jwt_utils.py

🔓 Endpoint
http
Copy
Edit
POST /login
JWT Payload Example
json
Copy
Edit
{
  "username": "analyst1",
  "role": "analyst",
  "exp": 1744474210
}
🤖 Chat Service
Port: 5101

Purpose:

Exposes /chat endpoint

Validates JWT (via decorators)

Generates LLM output using llama-cpp-python

Logging: Requests/responses logged and rotated (loguru)

Environment Variables
env
Copy
Edit
MODEL_PATH=/app/models/TinyLLAMA/tinyllama-1.1b-chat-v1.0.Q4_K_S.gguf
LOG_DIR=/app/log_service/responses_logs
🌐 NGINX Reverse Proxy
HTTPS Port: 8443

Features:

TLS termination (self-signed or custom cert)

CORS headers properly managed

Proxies /login and /chat to their respective services

External Access
bash
Copy
Edit
https://localhost:8443/login
https://localhost:8443/chat
🐳 Docker Compose Overview
yaml
Copy
Edit
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
🧪 API Testing
🔑 Login
bash
Copy
Edit
curl -k https://localhost:8443/login \
  -H "Content-Type: application/json" \
  -d '{"username": "analyst1", "password": "pass123"}'
🤖 Chat
bash
Copy
Edit
curl -k https://localhost:8443/chat \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Give me tips for improving banking risk assessment."}'
🔐 Security Measures
JWT + RBAC-based endpoint protection

TLS (HTTPS) on all public interfaces

Services isolated in internal network bridge

CORS headers and Vary: Origin managed carefully

Model path and secret values isolated via env/volumes

Log rotation using loguru (production-ready)

🛠 Future Enhancements
 Add Refresh Token logic with expiry renewal

 RBAC Dashboard for role management (admin UI)

 Centralized monitoring (Prometheus + Grafana)

 Integrated React frontend (already scaffolded)

 GitHub Actions CI/CD (auto-build + push)




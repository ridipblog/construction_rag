# Complete VPS Deployment Guide: Construction RAG Agent
## Production Setup on Ubuntu 22.04 / 24.04 LTS (FastAPI + Ollama + PostgreSQL pgvector + Nginx + SSL)

This guide provides copy-paste commands to deploy your **Construction Estimation RAG AI Agent** to a production Linux VPS (DigitalOcean, AWS EC2, Hetzner, Linode, Contabo, etc.).

---

## 1. VPS Specifications Recommendation

| Resource | Minimum | Recommended |
|---|---|---|
| **CPU** | 2 vCPUs | 4 vCPUs |
| **RAM** | 8 GB | 16 GB (Optimal for local Ollama models) |
| **Storage** | 40 GB SSD | 80 GB NVMe SSD |
| **OS** | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |

---

## 2. Step 1: Initial Server Update & Dependencies

Connect to your VPS via SSH:
```bash
ssh root@YOUR_SERVER_IP
```

Update system packages and install essential build tools and Python:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git ufw build-essential \
    python3 python3-venv python3-pip python3-dev \
    libpq-dev nginx certbot python3-certbot-nginx
```

---

## 3. Step 2: Install and Configure Ollama (Local AI)

### A. Install Ollama via Official Script
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### B. Enable and Start Ollama Service
```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

### C. Download Required Models
Download the 768-dim embedding model and the civil engineering reasoning model:
```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

Verify models are installed:
```bash
ollama list
```

---

## 4. Step 3: Install Docker & Run PostgreSQL with `pgvector`

### A. Install Docker Engine
```bash
curl -fsSL https://get.docker.com | sh
sudo systemctl enable docker
sudo systemctl start docker
```

### B. Launch PostgreSQL 17 + pgvector Container
Run the container with automatic restart and persistent volume:
```bash
docker run -d \
  --name construction-postgres \
  --restart always \
  -p 127.0.0.1:5433:5432 \
  -e POSTGRES_USER=construction_user \
  -e POSTGRES_PASSWORD=SuperStrongProductionPassword2026! \
  -e POSTGRES_DB=construction_rag \
  -v construction_pgdata:/var/lib/postgresql/data \
  pgvector/pgvector:pg17
```

> **Security Note:** Binding to `127.0.0.1:5433` ensures your database is only accessible locally and blocked from the public internet.

Verify container is running:
```bash
docker ps
```

---

## 5. Step 4: Deploy the RAG Agent Application Code

### A. Create Project Directory
```bash
sudo mkdir -p /var/www/construction-rag
sudo chown -R $USER:$USER /var/www/construction-rag
cd /var/www/construction-rag
```

### B. Copy or Clone Your Codebase
You can clone from Git or upload using `rsync` / `scp`:
```bash
# Example if using git:
# git clone <your-repo-url> /var/www/construction-rag
```

Ensure your directory contains:
```
/var/www/construction-rag/
├── app/
├── documents/
├── requirements.txt
├── seed_database.py
└── .env
```

### C. Create Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install python-multipart
```

---

## 6. Step 5: Configure Production Environment Variables (`.env`)

Create or edit `/var/www/construction-rag/.env`:
```bash
nano /var/www/construction-rag/.env
```

Paste the following production configuration:
```env
# PostgreSQL + pgvector Configuration
DB_HOST=127.0.0.1
DB_PORT=5433
DB_USER=construction_user
DB_PASSWORD=SuperStrongProductionPassword2026!
DB_NAME=construction_rag

# Ollama Configuration
OLLAMA_BASE_URL=http://127.0.0.1:11434
EMBEDDING_MODEL=nomic-embed-text
LLM_MODEL=llama3.2:3b

# Application Configuration
APP_HOST=127.0.0.1
APP_PORT=8001
DEBUG=False
```

---

## 7. Step 6: Seed Indian Construction Standards into pgvector

Run the seed script inside your virtual environment:
```bash
cd /var/www/construction-rag
source .venv/bin/activate
python seed_database.py
```

Expected output:
```text
============================================================
Result: {'status': 'success', 'indexed_count': 8, 'total_documents': 8}
Knowledge base verified and ready!
============================================================
```

---

## 8. Step 7: Configure Systemd Daemon (Auto-Start on Boot)

Create a systemd service to keep the FastAPI server running 24/7 and restart automatically on crashes or server reboots:

```bash
sudo nano /etc/systemd/system/construction-rag.service
```

Paste the following configuration:
```ini
[Unit]
Description=Construction RAG Estimation Agent FastAPI Service
After=network.target docker.service ollama.service
Requires=docker.service ollama.service

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/construction-rag
EnvironmentFile=/var/www/construction-rag/.env
ExecStart=/var/www/construction-rag/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001 --workers 2
Restart=always
RestartSec=5
StandardOutput=append:/var/log/construction-rag.log
StandardError=append:/var/log/construction-rag.err

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable construction-rag
sudo systemctl start construction-rag
```

Check service status:
```bash
sudo systemctl status construction-rag
```

View live logs anytime:
```bash
tail -f /var/log/construction-rag.log
```

---

## 9. Step 8: Configure Nginx as a Reverse Proxy with SSL (HTTPS)

### A. Create Nginx Configuration
Replace `api.yourdomain.com` with your subdomain or server IP:

```bash
sudo nano /etc/nginx/sites-available/construction-rag.conf
```

Paste the following:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com; # Or your server's public IP

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeouts for LLM engineering synthesis
        proxy_connect_timeout 180s;
        proxy_send_timeout 180s;
        proxy_read_timeout 180s;
    }
}
```

Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/construction-rag.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### B. Secure with Free Let's Encrypt SSL (HTTPS)
*(Requires a domain name pointing to your VPS IP)*:
```bash
sudo certbot --nginx -d api.yourdomain.com
```

---

## 10. Step 9: Firewall Setup (UFW Security)

Lock down all internal ports so database and Ollama cannot be accessed externally:

```bash
# Allow SSH, HTTP, and HTTPS
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
```

---

## 11. Step 10: Connect from Laravel Application

In your Laravel application's `.env`:

```env
# If hosted on separate servers:
CONSTRUCTION_AI_URL=https://api.yourdomain.com
CONSTRUCTION_AI_TIMEOUT=120
```

Test from Laravel:
```bash
php artisan tinker
```
```php
$agent = new App\Services\ConstructionAgentService();
$health = $agent->checkAgentHealth();
// Returns: ["status" => "operational", "indexed_documents_count" => 8, ...]
```

---

## 12. Maintenance & Quick Reference Commands

| Action | Command |
|---|---|
| **Restart AI Agent API** | `sudo systemctl restart construction-rag` |
| **View Live API Logs** | `sudo journalctl -u construction-rag -f` |
| **Restart Database** | `docker restart construction-postgres` |
| **Restart Ollama** | `sudo systemctl restart ollama` |
| **Backup PostgreSQL DB** | `docker exec construction-postgres pg_dump -U construction_user construction_rag > backup_$(date +%F).sql` |
| **Restore Database** | `docker exec -i construction-postgres psql -U construction_user construction_rag < backup.sql` |
| **Upload New PDF** | `curl -X POST "https://api.yourdomain.com/api/construction/upload-pdf" -F "file=@document.pdf" -F "category=standards"` |


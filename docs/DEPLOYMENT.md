# Guia de Implantação - Kairos

## Visão Geral

Este guia fornece instruções detalhadas para implantar o Kairos em diferentes ambientes, desde desenvolvimento local até produção.

## Ambientes

### 1. Desenvolvimento Local
Para desenvolvimento e testes locais.

### 2. Staging
Ambiente de homologação para testes finais.

### 3. Produção
Ambiente de produção para usuários finais.

## Pré-requisitos

### Servidor
- **Sistema Operacional**: Ubuntu 20.04+ ou CentOS 8+
- **RAM**: Mínimo 2GB, recomendado 4GB+
- **Armazenamento**: Mínimo 20GB SSD
- **CPU**: 2 cores mínimo

### Software
- **Node.js**: 18.0.0+
- **Python**: 3.11.0+
- **Nginx**: 1.18.0+ (para produção)
- **PM2**: Para gerenciamento de processos Node.js
- **Supervisor**: Para gerenciamento de processos Python

## Implantação Local

### 1. Preparação do Ambiente

```bash
# Clone do repositório
git clone https://github.com/GabrielJaccoud/Kairos.git
cd Kairos

# Configuração de permissões
chmod +x scripts/setup.sh
```

### 2. Frontend

```bash
# Instalar dependências
npm install

# Executar em desenvolvimento
npm start

# Build para produção
npm run build
```

### 3. Backend

```bash
# Navegar para backend
cd backend/kairos-backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
python -c "from src.main import db; db.create_all()"

# Executar servidor
python src/main.py
```

### 4. AI Engine

```bash
# Navegar para AI engine
cd ai-engine

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Testar componentes
python task-optimizer.py
```

## Implantação em Servidor

### 1. Preparação do Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências do sistema
sudo apt install -y nginx python3 python3-pip python3-venv nodejs npm git

# Instalar PM2 globalmente
sudo npm install -g pm2

# Instalar Supervisor
sudo apt install -y supervisor
```

### 2. Configuração do Usuário

```bash
# Criar usuário para aplicação
sudo adduser kairos
sudo usermod -aG sudo kairos

# Mudar para usuário kairos
sudo su - kairos

# Configurar SSH keys (se necessário)
ssh-keygen -t rsa -b 4096 -C "kairos@servidor"
```

### 3. Deploy do Código

```bash
# Clone do repositório
cd /home/kairos
git clone https://github.com/GabrielJaccoud/Kairos.git
cd Kairos

# Configurar permissões
sudo chown -R kairos:kairos /home/kairos/Kairos
```

### 4. Configuração do Frontend

```bash
# Instalar dependências
npm install

# Build para produção
npm run build

# Configurar Nginx
sudo nano /etc/nginx/sites-available/kairos
```

**Configuração do Nginx** (`/etc/nginx/sites-available/kairos`):

```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;
    
    root /home/kairos/Kairos/build;
    index index.html index.htm;
    
    # Configuração para SPA (Single Page Application)
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy para API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # Configuração de cache para assets estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Configuração de segurança
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/kairos /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Configuração do Backend

```bash
# Navegar para backend
cd /home/kairos/Kairos/backend/kairos-backend

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
nano .env
```

**Arquivo `.env`**:
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=sua-chave-secreta-muito-segura
DATABASE_URL=sqlite:///kairos.db
CORS_ORIGINS=https://seu-dominio.com
```

```bash
# Configurar banco de dados
python -c "from src.main import db; db.create_all()"

# Configurar Supervisor
sudo nano /etc/supervisor/conf.d/kairos-backend.conf
```

**Configuração do Supervisor** (`/etc/supervisor/conf.d/kairos-backend.conf`):

```ini
[program:kairos-backend]
command=/home/kairos/Kairos/backend/kairos-backend/venv/bin/python src/main.py
directory=/home/kairos/Kairos/backend/kairos-backend
user=kairos
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/kairos-backend.log
environment=PATH="/home/kairos/Kairos/backend/kairos-backend/venv/bin"
```

```bash
# Recarregar e iniciar Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start kairos-backend
```

### 6. Configuração do AI Engine

```bash
# Navegar para AI engine
cd /home/kairos/Kairos/ai-engine

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar como serviço (opcional)
sudo nano /etc/supervisor/conf.d/kairos-ai.conf
```

**Configuração do AI Engine** (`/etc/supervisor/conf.d/kairos-ai.conf`):

```ini
[program:kairos-ai]
command=/home/kairos/Kairos/ai-engine/venv/bin/python task-optimizer.py
directory=/home/kairos/Kairos/ai-engine
user=kairos
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/kairos-ai.log
environment=PATH="/home/kairos/Kairos/ai-engine/venv/bin"
```

## SSL/HTTPS (Produção)

### 1. Instalar Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 2. Obter Certificado SSL

```bash
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
```

### 3. Configurar Renovação Automática

```bash
# Testar renovação
sudo certbot renew --dry-run

# Configurar cron job
sudo crontab -e
```

Adicionar linha ao crontab:
```
0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoramento

### 1. Logs

```bash
# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs do Backend
sudo tail -f /var/log/kairos-backend.log

# Logs do AI Engine
sudo tail -f /var/log/kairos-ai.log

# Logs do Sistema
sudo journalctl -u nginx -f
sudo journalctl -u supervisor -f
```

### 2. Status dos Serviços

```bash
# Status do Nginx
sudo systemctl status nginx

# Status do Supervisor
sudo supervisorctl status

# Status dos processos Kairos
sudo supervisorctl status kairos-backend
sudo supervisorctl status kairos-ai
```

### 3. Monitoramento de Recursos

```bash
# Uso de CPU e memória
htop

# Espaço em disco
df -h

# Processos Python
ps aux | grep python

# Conexões de rede
netstat -tulpn | grep :80
netstat -tulpn | grep :5000
```

## Backup

### 1. Banco de Dados

```bash
# Script de backup
nano /home/kairos/backup-db.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/kairos/backups"
DB_PATH="/home/kairos/Kairos/backend/kairos-backend/kairos.db"

mkdir -p $BACKUP_DIR
cp $DB_PATH $BACKUP_DIR/kairos_$DATE.db

# Manter apenas os últimos 7 backups
find $BACKUP_DIR -name "kairos_*.db" -mtime +7 -delete

echo "Backup criado: kairos_$DATE.db"
```

```bash
chmod +x /home/kairos/backup-db.sh

# Configurar cron job para backup diário
crontab -e
```

Adicionar ao crontab:
```
0 2 * * * /home/kairos/backup-db.sh
```

### 2. Código Fonte

```bash
# Backup do código (se não usando Git)
tar -czf /home/kairos/backups/kairos-code-$(date +%Y%m%d).tar.gz /home/kairos/Kairos
```

## Atualizações

### 1. Atualização do Frontend

```bash
cd /home/kairos/Kairos

# Pull das mudanças
git pull origin main

# Instalar novas dependências (se houver)
npm install

# Build
npm run build

# Reiniciar Nginx
sudo systemctl reload nginx
```

### 2. Atualização do Backend

```bash
cd /home/kairos/Kairos

# Pull das mudanças
git pull origin main

# Ativar ambiente virtual
cd backend/kairos-backend
source venv/bin/activate

# Instalar novas dependências (se houver)
pip install -r requirements.txt

# Executar migrações (se houver)
# python migrate.py

# Reiniciar serviço
sudo supervisorctl restart kairos-backend
```

### 3. Atualização do AI Engine

```bash
cd /home/kairos/Kairos

# Pull das mudanças
git pull origin main

# Ativar ambiente virtual
cd ai-engine
source venv/bin/activate

# Instalar novas dependências (se houver)
pip install -r requirements.txt

# Reiniciar serviço (se configurado)
sudo supervisorctl restart kairos-ai
```

## Troubleshooting

### Problemas Comuns

#### 1. Erro 502 Bad Gateway
```bash
# Verificar se backend está rodando
sudo supervisorctl status kairos-backend

# Verificar logs
sudo tail -f /var/log/kairos-backend.log

# Reiniciar backend
sudo supervisorctl restart kairos-backend
```

#### 2. Erro de Permissões
```bash
# Corrigir permissões
sudo chown -R kairos:kairos /home/kairos/Kairos
sudo chmod -R 755 /home/kairos/Kairos
```

#### 3. Erro de Dependências Python
```bash
# Recriar ambiente virtual
cd /home/kairos/Kairos/backend/kairos-backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Erro de Build do Frontend
```bash
# Limpar cache e reinstalar
cd /home/kairos/Kairos
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Comandos Úteis

```bash
# Reiniciar todos os serviços
sudo systemctl restart nginx
sudo supervisorctl restart all

# Verificar portas em uso
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :5000

# Verificar espaço em disco
df -h
du -sh /home/kairos/Kairos

# Verificar logs em tempo real
sudo tail -f /var/log/nginx/error.log /var/log/kairos-backend.log
```

## Segurança

### 1. Firewall

```bash
# Configurar UFW
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw status
```

### 2. Atualizações de Segurança

```bash
# Configurar atualizações automáticas
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 3. Hardening do Servidor

```bash
# Desabilitar root login via SSH
sudo nano /etc/ssh/sshd_config
# PermitRootLogin no

# Configurar fail2ban
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Performance

### 1. Otimização do Nginx

```nginx
# Adicionar ao bloco server
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

# Cache de assets
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 2. Otimização do Backend

```python
# Configurações de produção no Flask
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['SQLALCHEMY_ECHO'] = False
```

---

*Guia atualizado em: Janeiro 2024*


# 部署指南

**Cancer Epidemiology Research To Lancet — 多环境部署方案**

本文档涵盖本地开发、服务器部署、Docker 容器化和生产环境配置的完整指南。

---

## 目录

- [环境要求](#环境要求)
- [快速部署](#快速部署)
- [本地开发环境](#本地开发环境)
- [服务器部署](#服务器部署)
- [Docker 部署](#docker-部署)
- [Nginx 反向代理](#nginx-反向代理)
- [系统服务 (systemd)](#系统服务-systemd)
- [生产环境优化](#生产环境优化)
- [监控与日志](#监控与日志)
- [备份策略](#备份策略)
- [故障排除](#故障排除)

---

## 环境要求

### 硬件要求

| 配置项     | 最低要求        | 推荐配置         |
|-----------|----------------|-----------------|
| CPU       | 1 核            | 2 核以上         |
| 内存       | 512 MB          | 2 GB 以上       |
| 磁盘       | 500 MB          | 2 GB 以上       |
| 网络       | 无特殊要求       | 稳定的网络连接    |

### 软件要求

| 软件       | 版本要求        | 说明                           |
|-----------|----------------|-------------------------------|
| Python    | 3.10+          | 推荐 3.12                      |
| pip       | 21.0+          | 随 Python 安装                  |
| 操作系统    | macOS / Linux  | Windows 需使用 WSL              |
| Git       | 2.0+           | 可选，用于版本管理               |

### Python 依赖

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
pandas>=2.1.0
numpy>=1.26.0
openpyxl>=3.1.0
xlrd>=2.0.0
scipy>=1.11.0
statsmodels>=0.14.0
matplotlib>=3.8.0
seaborn>=0.13.0
plotly>=5.18.0
python-docx>=1.1.0
```

---

## 快速部署

### 一键脚本部署 (推荐)

```bash
# 1. 进入项目目录
cd oncology-global-data-to-lancet

# 2. 一键部署 (自动安装依赖并启动)
chmod +x deploy.sh
./deploy.sh quick
```

### deploy.sh 支持的命令

| 命令              | 说明                    |
|------------------|------------------------|
| `./deploy.sh`            | 默认执行 start         |
| `./deploy.sh start`      | 启动服务               |
| `./deploy.sh stop`       | 停止服务               |
| `./deploy.sh restart`    | 重启服务               |
| `./deploy.sh status`     | 查看运行状态            |
| `./deploy.sh logs`       | 查看最近日志            |
| `./deploy.sh install`    | 仅安装依赖              |
| `./deploy.sh quick`      | 安装依赖 + 启动服务     |

### 自定义参数

```bash
# 指定端口
PORT=9000 ./deploy.sh start

# 指定 Python 版本
PYTHON=python3.11 ./deploy.sh start

# 指定绑定地址
HOST=127.0.0.1 ./deploy.sh start

# 组合使用
PORT=9000 HOST=127.0.0.1 PYTHON=python3.12 ./deploy.sh start
```

---

## 本地开发环境

### 方式一：直接运行

```bash
# 安装依赖
pip3.12 install --break-system-packages -r requirements.txt

# 启动 (开发模式，支持热重载)
python3.12 run.py
```

### 方式二：虚拟环境 (推荐)

```bash
# 创建虚拟环境
python3.12 -m venv venv

# 激活虚拟环境
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows (WSL)

# 安装依赖
pip install -r requirements.txt

# 启动
python run.py

# 退出虚拟环境
deactivate
```

### 方式三：使用 conda

```bash
# 创建 conda 环境
conda create -n oncology python=3.12
conda activate oncology

# 安装依赖
pip install -r requirements.txt

# 启动
python run.py
```

### 开发模式配置

在 `run.py` 中设置 `reload=True` 可启用代码热重载:

```python
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8002,
    reload=True  # 开发模式
)
```

---

## 服务器部署

### 1. 环境准备

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.12 python3.12-venv python3-pip git

# CentOS/RHEL
sudo yum update -y
sudo yum install -y python3.12 python3-pip git
```

### 2. 克隆项目

```bash
cd /opt
git clone https://github.com/MoKangMedical/oncology-global-data-to-lancet.git
cd oncology-global-data-to-lancet
```

### 3. 安装依赖

```bash
# 推荐使用虚拟环境
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. 启动服务

```bash
# 前台运行 (测试用)
python run.py

# 后台运行 (生产用)
nohup python run.py > output/server.log 2>&1 &
echo $! > .pid
```

### 5. 验证

```bash
curl http://localhost:8002/health
```

---

## Docker 部署

### Dockerfile

在项目根目录创建 `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 创建输出目录
RUN mkdir -p output/charts output/papers output/exports app/static

# 暴露端口
EXPOSE 8002

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# 启动命令
CMD ["python", "run.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  oncology-app:
    build: .
    container_name: oncology-to-lancet
    ports:
      - "8002:8002"
    environment:
      - PORT=8002
    volumes:
      - ./output:/app/output
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Docker 命令

```bash
# 构建镜像
docker build -t oncology-to-lancet .

# 运行容器
docker run -d -p 8002:8002 --name oncology oncology-to-lancet

# 使用 docker-compose
docker-compose up -d

# 查看日志
docker logs -f oncology

# 停止
docker-compose down
```

---

## Nginx 反向代理

生产环境建议使用 Nginx 作为反向代理，提供 HTTPS 和负载均衡。

### Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL 证书
    ssl_certificate /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # 代理设置
    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 文件上传大小限制
        client_max_body_size 50M;
    }

    # 静态文件缓存
    location /static/ {
        proxy_pass http://127.0.0.1:8002/static/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 安装与配置 Nginx

```bash
# Ubuntu/Debian
sudo apt install -y nginx

# 复制配置
sudo cp nginx.conf /etc/nginx/sites-available/oncology
sudo ln -s /etc/nginx/sites-available/oncology /etc/nginx/sites-enabled/

# 测试并重载
sudo nginx -t
sudo systemctl reload nginx
```

---

## 系统服务 (systemd)

### 创建服务文件

```bash
sudo nano /etc/systemd/system/oncology.service
```

### 服务配置

```ini
[Unit]
Description=Cancer Epidemiology Research To Lancet
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/oncology-global-data-to-lancet
Environment=PATH=/opt/oncology-global-data-to-lancet/venv/bin:/usr/bin
Environment=PORT=8002
ExecStart=/opt/oncology-global-data-to-lancet/venv/bin/python run.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 管理命令

```bash
# 启用并启动
sudo systemctl daemon-reload
sudo systemctl enable oncology
sudo systemctl start oncology

# 查看状态
sudo systemctl status oncology

# 查看日志
sudo journalctl -u oncology -f

# 重启
sudo systemctl restart oncology
```

---

## 生产环境优化

### Uvicorn Workers

使用多 Worker 提升并发性能:

```python
# 修改 run.py
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1

uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8002,
    workers=workers,
    access_log=True,
    log_level="info"
)
```

### gunicorn (可选)

```bash
pip install gunicorn

gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8002 \
  --access-logfile output/access.log \
  --error-logfile output/error.log
```

### 环境变量配置

创建 `.env` 文件:

```bash
# 服务配置
PORT=8002
HOST=0.0.0.0
WORKERS=4
LOG_LEVEL=info

# 输出目录
OUTPUT_DIR=output
CHARTS_DIR=output/charts
PAPERS_DIR=output/papers
EXPORTS_DIR=output/exports

# CORS (生产环境限制来源)
CORS_ORIGINS=https://your-domain.com
```

---

## 监控与日志

### 日志管理

```bash
# 查看应用日志
tail -f output/server.log

# systemd 日志
sudo journalctl -u oncology -f --since "1 hour ago"

# 日志轮转 (logrotate)
sudo nano /etc/logrotate.d/oncology
```

logrotate 配置:

```
/opt/oncology-global-data-to-lancet/output/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 640 www-data www-data
}
```

### 健康检查

```bash
# 手动检查
curl http://localhost:8002/health

# 定时检查脚本
#!/bin/bash
if ! curl -sf http://localhost:8002/health > /dev/null; then
    echo "Service down, restarting..."
    systemctl restart oncology
fi
```

### 资源监控

```bash
# 查看进程资源
top -p $(cat .pid)

# 端口占用
lsof -i:8002

# 磁盘使用
du -sh output/
```

---

## 备份策略

### 自动备份脚本

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backup/oncology"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# 备份输出文件
tar czf $BACKUP_DIR/output_$DATE.tar.gz output/

# 备份配置
cp requirements.txt $BACKUP_DIR/
cp deploy.sh $BACKUP_DIR/

# 保留最近 30 天的备份
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/output_$DATE.tar.gz"
```

### 定时备份

```bash
# 添加 crontab
crontab -e

# 每天凌晨 2 点备份
0 2 * * * /opt/oncology-global-data-to-lancet/backup.sh
```

---

## 故障排除

### 端口被占用

```bash
# 查找占用进程
lsof -ti:8002

# 强制释放
kill -9 $(lsof -ti:8002)

# 使用其他端口
PORT=9000 ./deploy.sh start
```

### 依赖安装失败

```bash
# 方案一: 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 方案二: 逐个安装
pip install fastapi uvicorn pandas numpy

# 方案三: 跳过已安装
pip install --upgrade -r requirements.txt
```

### Python 版本不兼容

```bash
# 检查版本
python3 --version

# 安装特定版本 (macOS)
brew install python@3.12

# 安装特定版本 (Ubuntu)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.12
```

### 图表中文乱码

```bash
# macOS
brew install font-noto-sans-cjk

# Ubuntu
sudo apt install fonts-noto-cjk

# 清除 Matplotlib 缓存
rm -rf ~/.cache/matplotlib

# 重启服务
./deploy.sh restart
```

### 内存不足

```bash
# 查看内存
free -h  # Linux
vm_stat  # macOS

# 增加 swap (Linux)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 文件上传失败

检查:
1. Nginx `client_max_body_size` 是否足够
2. 磁盘空间是否充足
3. 文件编码是否为 UTF-8

---

## 网络架构图

```
                    Internet
                       |
                    [Nginx]
                    (443/80)
                       |
               [Uvicorn Workers]
               (8002, 多 Worker)
                       |
            +----------+----------+
            |          |          |
        [统计引擎]  [可视化]  [论文生成]
            |          |          |
        [Pandas]  [Matplotlib] [模板引擎]
        [SciPy]   [Seaborn]
        [NumPy]   [Plotly]
                       |
                  [输出文件系统]
                  output/
                  ├── charts/
                  ├── papers/
                  └── exports/
```

---

如需进一步帮助，请查阅:
- [README.md](README.md) — 项目概览
- [USER_GUIDE.md](USER_GUIDE.md) — 用户手册
- [CHANGELOG.md](CHANGELOG.md) — 版本更新日志

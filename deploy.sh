#!/bin/bash
# Cancer Epidemiology Research To Lancet - Deploy Script

set -e

PORT=${PORT:-8002}
HOST=${HOST:-0.0.0.0}
PYTHON=${PYTHON:-python3.12}

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  Cancer Epidemiology Research To Lancet${NC}"
echo -e "${GREEN}  肿瘤学全球数据到柳叶刀${NC}"
echo -e "${GREEN}============================================================${NC}"

# Check Python
if ! command -v $PYTHON &> /dev/null; then
    echo -e "${RED}Error: $PYTHON not found${NC}"
    exit 1
fi

# Create directories
mkdir -p output/{charts,papers,exports} app/static

# Install dependencies
install_deps() {
    echo -e "${YELLOW}Installing dependencies...${NC}"
    $PYTHON -m pip install --break-system-packages -i https://pypi.tuna.tsinghua.edu.cn/simple -q \
        fastapi uvicorn pandas numpy scipy statsmodels matplotlib seaborn plotly \
        openpyxl xlrd python-multipart python-docx 2>/dev/null || \
    $PYTHON -m pip install --break-system-packages -q \
        fastapi uvicorn pandas numpy scipy statsmodels matplotlib seaborn plotly \
        openpyxl xlrd python-multipart python-docx
    echo -e "${GREEN}Dependencies installed${NC}"
}

# Stop existing
stop_existing() {
    if [ -f .pid ]; then
        kill $(cat .pid) 2>/dev/null || true
        rm .pid
    fi
    lsof -ti :$PORT | xargs kill -9 2>/dev/null || true
}

# Start server
start_server() {
    stop_existing
    echo -e "${YELLOW}Starting server on $HOST:$PORT...${NC}"
    nohup $PYTHON -c "
import uvicorn
uvicorn.run('app.main:app', host='$HOST', port=$PORT)
" > output/server.log 2>&1 &
    echo $! > .pid
    sleep 2
    if curl -s http://localhost:$PORT/health > /dev/null 2>&1; then
        echo -e "${GREEN}Server started successfully!${NC}"
        echo -e "${GREEN}  Frontend: http://localhost:$PORT${NC}"
        echo -e "${GREEN}  API Docs: http://localhost:$PORT/api/docs${NC}"
    else
        echo -e "${RED}Server failed to start. Check output/server.log${NC}"
        exit 1
    fi
}

case "${1:-start}" in
    install) install_deps ;;
    start) start_server ;;
    stop) stop_existing; echo -e "${GREEN}Stopped${NC}" ;;
    restart) start_server ;;
    status)
        if curl -s http://localhost:$PORT/health > /dev/null 2>&1; then
            echo -e "${GREEN}Running on port $PORT${NC}"
        else
            echo -e "${RED}Not running${NC}"
        fi
        ;;
    logs) tail -50 output/server.log ;;
    quick)
        install_deps
        start_server
        ;;
    *)
        echo "Usage: ./deploy.sh [install|start|stop|restart|status|logs|quick]"
        ;;
esac

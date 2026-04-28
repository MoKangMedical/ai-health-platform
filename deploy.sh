#!/bin/bash
# AI健康平台部署脚本

set -e

echo "=========================================="
echo "  AI健康平台部署脚本"
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查Python版本
check_python() {
    echo -e "${YELLOW}检查Python版本...${NC}"
    if command -v python3.12 &> /dev/null; then
        PYTHON=python3.12
    elif command -v python3 &> /dev/null; then
        PYTHON=python3
    else
        echo -e "${RED}错误: 未找到Python${NC}"
        exit 1
    fi
    echo -e "${GREEN}Python版本: $($PYTHON --version)${NC}"
}

# 创建虚拟环境
setup_venv() {
    echo -e "${YELLOW}设置虚拟环境...${NC}"
    if [ ! -d "venv" ]; then
        $PYTHON -m venv venv
        echo -e "${GREEN}虚拟环境已创建${NC}"
    fi
    source venv/bin/activate
    echo -e "${GREEN}虚拟环境已激活${NC}"
}

# 安装依赖
install_deps() {
    echo -e "${YELLOW}安装依赖...${NC}"
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo -e "${GREEN}依赖安装完成${NC}"
}

# 初始化数据库
init_database() {
    echo -e "${YELLOW}初始化数据库...${NC}"
    $PYTHON -c "from src.models.database import init_db; init_db()"
    echo -e "${GREEN}数据库初始化完成${NC}"
}

# 运行测试
run_tests() {
    echo -e "${YELLOW}运行测试...${NC}"
    $PYTHON -m pytest tests/ -v
    echo -e "${GREEN}测试完成${NC}"
}

# 启动服务
start_service() {
    echo -e "${YELLOW}启动服务...${NC}"
    echo -e "${GREEN}API文档: http://localhost:8200/docs${NC}"
    echo -e "${GREEN}控制台: http://localhost:8200${NC}"
    $PYTHON -m src.api.main
}

# Docker部署
deploy_docker() {
    echo -e "${YELLOW}Docker部署...${NC}"
    docker-compose up -d --build
    echo -e "${GREEN}Docker部署完成${NC}"
    echo -e "${GREEN}API: http://localhost:8200${NC}"
    echo -e "${GREEN}Nginx: http://localhost${NC}"
}

# 显示帮助
show_help() {
    echo "用法: ./deploy.sh [命令]"
    echo ""
    echo "命令:"
    echo "  setup     - 安装依赖并初始化"
    echo "  start     - 启动服务"
    echo "  test      - 运行测试"
    echo "  docker    - Docker部署"
    echo "  help      - 显示帮助"
}

# 主流程
case "${1:-setup}" in
    setup)
        check_python
        setup_venv
        install_deps
        init_database
        echo -e "${GREEN}设置完成！运行 './deploy.sh start' 启动服务${NC}"
        ;;
    start)
        check_python
        source venv/bin/activate 2>/dev/null || true
        start_service
        ;;
    test)
        check_python
        source venv/bin/activate 2>/dev/null || true
        run_tests
        ;;
    docker)
        deploy_docker
        ;;
    help|*)
        show_help
        ;;
esac

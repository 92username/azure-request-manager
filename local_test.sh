#!/bin/bash

# Script para testar o Azure Request Manager localmente antes do deploy

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}==== Iniciando teste local do Azure Request Manager ====${NC}"

# Verificar se o .env existe
if [ ! -f .env ]; then
  echo -e "${RED}Arquivo .env não encontrado. Criando a partir dos valores padrão...${NC}"
  cp -v .env.example .env 2>/dev/null || {
    echo -e "${YELLOW}Criando arquivo .env com valores padrão${NC}"
    echo "# API Configuration
API_URL=https://example.com/api
REQUEST_INTERVAL=30
FAILURE_RATE=10
FAILURE_MODES=timeout,500

# Grafana Credentials
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin

# Prometheus Configuration
PROMETHEUS_PORT=9090" > .env
  }
  echo -e "${YELLOW}Criado arquivo .env. Por favor, revise os valores antes de continuar.${NC}"
  echo -e "${YELLOW}IMPORTANTE: Atualize o API_URL para o endpoint correto${NC}"
  read -p "Pressione Enter para continuar, ou Ctrl+C para cancelar e editar o arquivo .env..."
fi

# Executar testes unitários
echo -e "${YELLOW}Executando testes unitários...${NC}"
pytest tests/ -v || {
  echo -e "${RED}Os testes falharam. Verifique os erros acima antes de continuar.${NC}"
  read -p "Pressione Enter para continuar assim mesmo, ou Ctrl+C para cancelar..."
}

# Construir as imagens Docker
echo -e "${YELLOW}Construindo imagens Docker...${NC}"
docker-compose build || {
  echo -e "${RED}Falha ao construir as imagens Docker. Verifique os erros acima.${NC}"
  exit 1
}

# Iniciar os serviços
echo -e "${YELLOW}Iniciando serviços...${NC}"
docker-compose up -d

# Verificar se os serviços estão rodando
echo -e "${YELLOW}Verificando status dos serviços...${NC}"
sleep 5
docker-compose ps

echo -e "${GREEN}==== Serviços iniciados ====${NC}"
echo -e "${GREEN}Acesse a interface web: http://localhost:5000${NC}"
echo -e "${GREEN}Grafana: http://localhost:3000 (login: $(grep GRAFANA_ADMIN_USER .env | cut -d= -f2) / $(grep GRAFANA_ADMIN_PASSWORD .env | cut -d= -f2))${NC}"
echo -e "${GREEN}Prometheus: http://localhost:9090${NC}"
echo 
echo -e "${YELLOW}Para parar os serviços, execute: docker-compose down${NC}"
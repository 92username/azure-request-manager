#!/bin/bash

# Script para testar o Azure Request Manager localmente antes do deploy usando Docker

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}==== Iniciando teste local do Azure Request Manager com Docker ====${NC}"

# Verificar se o Docker está em execução
if ! docker info > /dev/null 2>&1; then
  echo -e "${RED}Docker não está em execução. Por favor, inicie o Docker e tente novamente.${NC}"
  exit 1
fi

# Verificar se o .env existe
if [ ! -f .env ]; then
  echo -e "${RED}Arquivo .env não encontrado. Criando com a URL fixa...${NC}"
  echo "# API Configuration
API_URL=http://191.234.214.44:8000
REQUEST_INTERVAL=30
FAILURE_RATE=10
FAILURE_MODES=timeout,500

# Grafana Credentials
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin

# Prometheus Configuration
PROMETHEUS_PORT=9090" > .env
  
  echo -e "${GREEN}Criado arquivo .env com a URL fixa: http://191.234.214.44:8000${NC}"
  echo -e "${YELLOW}Você pode editar o arquivo .env para ajustar as configurações se necessário${NC}"
fi

# Verificar e atualizar arquivos de configuração para garantir URL fixa
echo -e "${YELLOW}Verificando que o requester.py está usando a URL fixa...${NC}"
if ! grep -q "FIXED_API_URL = \"http://191.234.214.44:8000\"" requester.py; then
  echo -e "${YELLOW}A URL fixa não foi encontrada em requester.py.${NC}"
  echo -e "${YELLOW}Certifique-se de que a aplicação está configurada para usar a URL fixa.${NC}"
fi

# Executar testes unitários antes de iniciar os contêineres
echo -e "${YELLOW}Executando testes unitários...${NC}"
docker run --rm -v $(pwd):/app -w /app python:3.9 bash -c "pip install pytest pytest-cov && pip install -r requirements.txt && pytest tests/ -v" || {
  echo -e "${RED}Os testes falharam. Verifique os erros acima antes de continuar.${NC}"
  read -p "Pressione Enter para continuar assim mesmo, ou Ctrl+C para cancelar..."
}

# Construir e iniciar os serviços
echo -e "${YELLOW}Construindo e iniciando serviços Docker...${NC}"
docker-compose build
docker-compose up -d

# Verificar se os serviços subiram corretamente
echo -e "${YELLOW}Verificando status dos serviços...${NC}"
sleep 5
docker-compose ps

echo -e "${GREEN}==== Ambiente de teste local iniciado com sucesso! ====${NC}"
echo -e "${GREEN}Acesse a interface web: http://localhost:5000${NC}"
echo -e "${GREEN}Métricas do Requester: http://localhost:8001/metrics${NC}"
echo -e "${GREEN}Prometheus: http://localhost:9090${NC}"
echo -e "${GREEN}Grafana: http://localhost:3000 (login: admin / admin)${NC}"
echo
echo -e "${YELLOW}Para ver logs em tempo real: docker-compose logs -f${NC}"
echo -e "${YELLOW}Para parar os serviços: docker-compose down${NC}"

# Criar um arquivo para facilitar a visualização dos logs
echo "#!/bin/bash
docker-compose logs -f \$@
" > view_logs.sh
chmod +x view_logs.sh

# Criar um arquivo para facilitar a parada dos serviços
echo "#!/bin/bash
docker-compose down
echo 'Serviços encerrados.'
" > stop_services.sh
chmod +x stop_services.sh

echo -e "${YELLOW}Scripts úteis criados:${NC}"
echo -e "${YELLOW}- ./view_logs.sh: Ver logs em tempo real${NC}"
echo -e "${YELLOW}- ./stop_services.sh: Parar todos os serviços${NC}"
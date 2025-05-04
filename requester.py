#!/usr/bin/env python3

import os
import time
import logging
import random
import requests
import json
from datetime import datetime
from prometheus_client import start_http_server, Counter, Histogram, Gauge

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/requester.log')
    ]
)
logger = logging.getLogger("azure_requester")

# Carregar configuração
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except Exception as e:
    logger.warning(f"Não foi possível carregar config.json: {e}")
    config = {}

# Variáveis de ambiente ou valores padrão
API_URL = os.environ.get("API_URL", "http://localhost:8000")
REQUEST_INTERVAL = int(os.environ.get("REQUEST_INTERVAL", "30"))
FAILURE_RATE = int(os.environ.get("FAILURE_RATE", "10"))
FAILURE_MODES = os.environ.get("FAILURE_MODES", "timeout,500").split(",")

# Métricas Prometheus
REQUEST_COUNT = Counter(
    'azure_request_count', 
    'Número total de requisições feitas à API do Azure', 
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'azure_request_latency_seconds', 
    'Latência das requisições à API do Azure',
    ['method', 'endpoint'],
    buckets=(0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, 15.0, 30.0, 60.0)
)

ERROR_COUNT = Counter(
    'azure_request_error_count', 
    'Número de erros nas requisições à API do Azure',
    ['method', 'endpoint', 'error_type']
)

API_UP = Gauge(
    'azure_api_up', 
    'Indica se a API do Azure está respondendo normalmente'
)

def simulate_failure():
    """Simula falhas baseadas na configuração."""
    if random.randint(1, 100) <= FAILURE_RATE:
        failure_mode = random.choice(FAILURE_MODES)
        logger.info(f"Simulando falha: {failure_mode}")
        
        if failure_mode == "timeout":
            raise requests.exceptions.Timeout("Tempo limite da requisição excedido")
        elif failure_mode == "connection_refused":
            raise requests.exceptions.ConnectionError("Conexão recusada")
        elif failure_mode == "500" or failure_mode == "server_error":
            response = requests.Response()
            response.status_code = 500
            response._content = b'{"error": "Internal Server Error"}'
            response.encoding = 'utf-8'
            return response
        elif failure_mode == "404":
            response = requests.Response()
            response.status_code = 404
            response._content = b'{"error": "Resource Not Found"}'
            response.encoding = 'utf-8'
            return response
    return None

def make_request():
    """Faz uma requisição à API do Azure e registra métricas."""
    endpoint = "/api/resource"
    method = "GET"
    url = f"{API_URL}{endpoint}"
    start_time = time.time()
    api_status = 0  # 0 = down, 1 = up
    
    try:
        # Verifica se devemos simular uma falha
        failure_response = simulate_failure()
        if failure_response:
            response = failure_response
        else:
            response = requests.get(url, timeout=10)
        
        status = str(response.status_code)
        
        # Registra métricas
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
        request_time = time.time() - start_time
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(request_time)
        
        # Registra erros para códigos 4xx e 5xx
        if response.status_code >= 400:
            error_type = "client_error" if response.status_code < 500 else "server_error"
            ERROR_COUNT.labels(method=method, endpoint=endpoint, error_type=error_type).inc()
            logger.error(f"Erro na requisição: {status} - {url}")
        else:
            api_status = 1  # API está funcionando
            logger.info(f"Requisição bem-sucedida: {status} - {url} ({request_time:.2f}s)")
            
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout na requisição: {url} - {e}")
        ERROR_COUNT.labels(method=method, endpoint=endpoint, error_type="timeout").inc()
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="timeout").inc()
        
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Erro de conexão: {url} - {e}")
        ERROR_COUNT.labels(method=method, endpoint=endpoint, error_type="connection_error").inc()
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="connection_error").inc()
        
    except Exception as e:
        logger.error(f"Erro inesperado: {url} - {e}")
        ERROR_COUNT.labels(method=method, endpoint=endpoint, error_type="unexpected_error").inc()
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status="error").inc()
    
    # Atualiza o status da API
    API_UP.set(api_status)
    
    return api_status

def main():
    """Função principal que inicia o servidor HTTP para métricas e faz requisições periódicas."""
    # Inicia servidor de métricas na porta 8001
    start_http_server(8001)
    logger.info(f"Servidor de métricas iniciado na porta 8001")
    logger.info(f"API URL: {API_URL}")
    logger.info(f"Intervalo entre requisições: {REQUEST_INTERVAL}s")
    logger.info(f"Taxa de falhas: {FAILURE_RATE}%")
    logger.info(f"Modos de falha: {FAILURE_MODES}")
    
    # Loop principal
    while True:
        make_request()
        time.sleep(REQUEST_INTERVAL)

if __name__ == "__main__":
    # Certifique-se de que o diretório de logs existe
    os.makedirs("logs", exist_ok=True)
    main()
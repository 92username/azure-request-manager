# Visão Geral do Projeto

Este projeto tem como objetivo demonstrar um pipeline completo de CI/CD, monitoramento e observabilidade de uma aplicação hospedada em uma VM na Azure, usando práticas modernas de DevOps.

## Componentes da Arquitetura

- **FastAPI (API alvo)**: hospedada na Azure. Endpoints conforme *main.py* no repositório.
- **Script gerador de requisições**: simula chamadas constantes à API.
- **Prometheus**: coleta métricas expostas pelo script e/ou pela API. Executado na VPS da Hostinger.
- **Grafana**: exibe visualmente os dados coletados. Também hospedado na VPS.
- **GitHub Actions**: realiza build, testes, lint, análise de segurança e deploy.
- **Docker Compose**: orquestra todos os serviços para fácil replicação.

## Fluxo de Operações

1. Alterações no código são commitadas no GitHub.  
2. GitHub Actions executa testes automatizados, análise de segurança e faz o deploy.  
3. A aplicação sobe na VM.  
4. O script gerador envia requisições periódicas para a API.  
5. As métricas dessas requisições são expostas em */metrics*.  
6. Prometheus coleta essas métricas.  
7. Grafana as exibe em dashboards em tempo real.

## Objetivo Educacional

Este projeto é uma vitrine prática de:

- Integração Contínua (CI)
- Entrega Contínua (CD)
- Monitoramento com Prometheus e Grafana
- Análise de código e segurança com linters e scanners
- Containerização e padronização com Docker
- Organização e documentação técnica

## Status Atual

- **API e GitHub Actions operacionais**.  
- **Script gerador** em fase de ajustes.  
- **Monitoramento e visualização** em desenvolvimento.
Com base no conteúdo dos arquivos `requisitos.md`, `overview.md` e no seu Canvas atualizado, aqui está o `README.md` inicial para o projeto **Azure Request Manager**:

---

````markdown
# Azure Request Manager

**Aplicativo leve e modular para simular requisições automáticas a uma API hospedada na Azure**, com suporte a simulação de falhas e monitoramento completo via Prometheus e Grafana.

---

## 📌 Visão Geral

Este projeto permite testar e monitorar uma API executando em uma VM da Azure. Ele simula requisições periódicas configuráveis, com possibilidade de gerar falhas intencionais (timeout, status 500, etc.). É ideal para cenários de teste de resiliência e observabilidade.

> A interface web leve em Flask permite ao usuário ajustar os parâmetros de execução do script em tempo real.

---

## 🧱 Arquitetura

- **FastAPI** — API de destino hospedada na Azure
- **Flask** — Interface web leve para configuração dos parâmetros de requisição
- **Script `requester.py`** — Dispara requisições periódicas com simulação de falhas
- **Prometheus** — Coleta métricas expostas pelo script
- **Grafana** — Visualiza os dados em tempo real
- **Docker Compose** — Orquestração de todos os serviços
- **GitHub Actions** — CI/CD com testes, lint, segurança e deploy automático

---

## 🚀 Funcionalidades

- [x] Simulação de tráfego HTTP para uma API
- [x] Configuração via formulário web (frequência, destino, falhas)
- [x] Exposição de métricas para Prometheus (`/metrics`)
- [x] Monitoramento via dashboard do Grafana
- [x] Integração com CI/CD automatizado no GitHub

---

## 🛠️ Requisitos

### Funcionais
- Geração automática de requisições à API
- Simulação de falhas (timeout, 500)
- Exposição de métricas
- Visualização no Grafana
- Interface web para controle
- CI/CD via GitHub Actions
- Orquestração com Docker Compose

### Não Funcionais
- Tolerância a falhas e logs persistentes
- Infraestrutura reprodutível
- Documentação completa
- Visualização acessível e protegida
- Monitoramento com latência < 10s

---

## 🔧 Execução local (com venv)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python webserver.py
````

---

## 🐳 Com Docker

```bash
docker-compose up --build
```

---

## 🧪 Status do Projeto

* ✅ API e CI/CD funcionando
* ⚙️ Script de requisições 
* 🔜 Integração total com interface Flask
* 📊 Prometheus e Grafana em implantação

---

## 🧠 Aprendizado e Objetivo Educacional

Este projeto é uma vitrine prática de:

* CI/CD com GitHub Actions
* Monitoramento moderno com Prometheus + Grafana
* Boas práticas com containers e arquitetura limpa
* Design simples, funcional e extensível

---

## 🔗 Contato

Mantenedor: [Vinicius (92username)](https://github.com/92username)
Domínio: [tamanduas.dev](https://tamanduas.dev)

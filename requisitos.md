# Requisitos Funcionais

- [ ] **RF - 01**: O sistema deve gerar requisições automáticas e configuráveis para a API hospedada na Azure.  
- [ ] **RF - 02**: O sistema deve simular falhas específicas como timeouts e respostas com status HTTP 500.  
- [ ] **RF - 03**: O sistema deve expor métricas em um endpoint `/metrics` para coleta pelo Prometheus.  
- [ ] **RF - 04**: O Prometheus deve ser capaz de coletar métricas do script de requisições e da API.  
- [ ] **RF - 05**: O Grafana deve apresentar os dados monitorados de forma visual em um dashboard customizado.  
- [ ] **RF - 06**: O projeto deve utilizar integração contínua (CI) e entrega contínua (CD) via GitHub Actions.  
- [ ] **RF - 07**: Todos os serviços (API, Prometheus, Grafana, script) devem ser containerizados e orquestrados via Docker Compose.  
- [ ] **RF - 08**: O sistema deve possuir uma interface web baseada em Django para o usuário configurar os parâmetros de envio de requisições (frequência, destino, modo de simulação de falha).

# Requisitos Não Funcionais

- [ ] **RNF - 01**: O sistema deve ser tolerante a falhas de conexão ou indisponibilidade temporária da API.  
- [ ] **RNF - 02**: Logs das requisições e erros devem ser armazenados para futura análise e auditoria.  
- [ ] **RNF - 03**: A infraestrutura deve ser capaz de ser reproduzida em outro ambiente de forma automática.  
- [ ] **RNF - 04**: A solução deve ser documentada para que qualquer desenvolvedor consiga iniciar e operar o sistema.  
- [ ] **RNF - 05**: A visualização por Grafana deve ser acessível por domínio próprio e protegida por autenticação.  
- [ ] **RNF - 06**: O sistema deve permitir monitoramento em tempo real com no máximo 10 segundos de defasagem.  

# Restrições

- [ ] **R - 01**: Manter a simplicidade da arquitetura, evitando serviços desnecessários.  
- [ ] **R - 02**: Utilizar apenas ferramentas open-source.  
- [ ] **R - 03**: O projeto será hospedado parcialmente em Azure (API) e parcialmente na VPS da Hostinger (observabilidade).
# Azure Request Manager

**A lightweight, modular application for simulating HTTP traffic to an Azure-hosted API**, with support for configurable failure simulation, metrics visualization, and containerized deployment.

## 📌 Overview

The Azure Request Manager is designed to test and monitor APIs running in Azure VMs. It generates configurable HTTP traffic with the ability to simulate failures (timeouts, HTTP 500 errors) at specified rates, making it ideal for testing resilience and observability setups.

The system includes:
- A Flask web interface for real-time configuration
- A request generator that exposes Prometheus metrics
- Complete monitoring stack with Prometheus and Grafana
- CI/CD integration via GitHub Actions

## 🚀 Features

- ✅ Configurable HTTP traffic generation
- ✅ Failure simulation (timeouts, HTTP 500 errors)
- ✅ Prometheus-compatible metrics endpoint
- ✅ Grafana dashboards for visualization
- ✅ Configuration via web interface
- ✅ Containerized deployment with Docker Compose
- ✅ CI/CD workflow with GitHub Actions

## 🏗️ Architecture

The application consists of the following components:

1. **Flask Web UI** - Port 5000
   - Configuration interface for request parameters
   - Real-time status updates

2. **Request Generator** - Port 8001
   - Sends periodic requests to target API
   - Simulates failures according to configuration
   - Exposes Prometheus metrics at `/metrics`

3. **Prometheus** - Port 9090
   - Collects metrics from the request generator
   - Provides querying and alerting

4. **Grafana** - Port 3000
   - Visualizes metrics from Prometheus
   - Pre-configured dashboards

## 🛠️ Local Setup

### Prerequisites

- Docker and Docker Compose
- Git

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/92username/azure-request-manager.git
   cd azure-request-manager
   ```

2. Start all services:
   ```bash
   docker-compose up -d
   ```

3. Access the components:
   - Web UI: http://localhost:5000
   - Metrics: http://localhost:8001/metrics
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (admin/admin)

### Configuration

Use the web interface at http://localhost:5000 to configure:

- **API Endpoint URL**: The target API to send requests to
- **Request Interval**: Time in seconds between requests (1-3600)
- **Failure Rate**: Percentage of requests that should fail (0-100)
- **Failure Modes**: Types of failures to simulate (timeouts, HTTP 500)

## 📊 Monitoring

### Available Metrics

- `azure_request_total`: Total number of requests made
- `azure_request_success`: Number of successful requests
- `azure_request_timeout`: Number of simulated timeouts
- `azure_request_error_500`: Number of simulated HTTP 500 errors
- `azure_request_duration_seconds`: Histogram of request durations

### Grafana Dashboard

The pre-configured Grafana dashboard includes:
- Request rates and latencies
- Success/failure statistics
- Detailed status breakdown

## 🧪 Development

### Local Development Environment

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the web UI:
   ```bash
   python webserver.py
   ```

4. Run the requester in another terminal:
   ```bash
   python requester.py
   ```

### Running Tests

```bash
pytest tests/
```

## 📦 Deployment

### Docker Compose

The included `docker-compose.yml` orchestrates all services:

```bash
docker-compose up -d  # Start all services
docker-compose logs -f requester  # Watch requester logs
docker-compose down  # Stop all services
```

### CI/CD with GitHub Actions

The repository includes a GitHub Actions workflow that:
1. Lints Python code
2. Runs unit tests
3. Builds Docker images
4. Handles deployment (requires configuration)

To configure deployment:
1. Add necessary secrets in GitHub
2. Uncomment and configure the deployment section in `.github/workflows/ci-cd.yml`

## 📄 License

This project uses open-source technologies and is available under the MIT License.

## 📝 Requirements

This implementation satisfies all specified requirements:
- **RF-01**: Configurable automated requests
- **RF-02**: Failure simulation (timeouts, HTTP 500)
- **RF-03**: Metrics endpoint `/metrics`
- **RF-04/05**: Prometheus & Grafana integration
- **RF-06**: CI/CD via GitHub Actions
- **RF-07**: Docker Compose for all services
- **RF-08**: Flask web interface for configuration
- **RNF-01–RNF-06**: Resilience, logging, reproducibility
- **R-01–R-03**: Architecture simplicity, OSS-only

## 🔗 Contact

Maintainer: [Vinicius (92username)](https://github.com/92username)
Domain: [tamanduas.dev](https://tamanduas.dev)

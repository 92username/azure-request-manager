import os
import json
import time
import random
import logging
import threading
import requests
from prometheus_client import start_http_server, Counter, Histogram

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("requester.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Define Prometheus metrics
TOTAL_REQUESTS = Counter("azure_request_total", "Total number of requests made")
SUCCESSFUL_REQUESTS = Counter("azure_request_success", "Number of successful requests")
SIMULATED_TIMEOUTS = Counter("azure_request_timeout", "Number of simulated timeouts")
SIMULATED_ERRORS_500 = Counter(
    "azure_request_error_500", "Number of simulated 500 errors"
)
REQUEST_DURATION = Histogram(
    "azure_request_duration_seconds", "Request duration in seconds"
)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def load_config():
    """Load configuration from config.json or use default values."""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        else:
            return {
                "api_url": "https://example.com/api",
                "interval_seconds": 30,
                "failure_rate": 10,
                "failure_modes": ["timeout", "500"],
            }
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {
            "api_url": "https://example.com/api",
            "interval_seconds": 30,
            "failure_rate": 10,
            "failure_modes": ["timeout", "500"],
        }


def should_simulate_failure(failure_rate):
    """Determine if this request should simulate a failure based on configured rate."""
    return random.random() < (failure_rate / 100.0)


def make_request(url, failure_rate, failure_modes):
    """Make an HTTP request to the given URL with possible failure simulation."""
    TOTAL_REQUESTS.inc()
    start_time = time.time()

    try:
        # Check if we should simulate a failure
        if should_simulate_failure(failure_rate):
            # Choose a failure mode randomly from the configured options
            if not failure_modes:
                # Default to both if none specified
                failure_modes = ["timeout", "500"]

            mode = random.choice(failure_modes)

            if mode == "timeout":
                logger.info(f"Simulating timeout for request to {url}")
                SIMULATED_TIMEOUTS.inc()
                time.sleep(10)  # Simulate a timeout
                raise requests.exceptions.Timeout("Simulated timeout")

            elif mode == "500":
                logger.info(f"Simulating 500 error for request to {url}")
                SIMULATED_ERRORS_500.inc()
                # Don't actually make the request, just simulate a 500 response
                duration = time.time() - start_time
                REQUEST_DURATION.observe(duration)
                return {
                    "success": False,
                    "status_code": 500,
                    "error": "Simulated 500 error",
                }

        # Make the actual request if no failure simulation
        response = requests.get(url, timeout=5)
        duration = time.time() - start_time
        REQUEST_DURATION.observe(duration)

        if response.status_code == 200:
            logger.info(
                f"Request to {url} succeeded with status code {response.status_code}"
            )
            SUCCESSFUL_REQUESTS.inc()
            return {
                "success": True,
                "status_code": response.status_code,
                "response_time": duration,
            }
        else:
            logger.warning(
                f"Request to {url} failed with status code {response.status_code}"
            )
            return {
                "success": False,
                "status_code": response.status_code,
                "error": f"HTTP error: {response.status_code}",
            }

    except requests.exceptions.Timeout as e:
        duration = time.time() - start_time
        REQUEST_DURATION.observe(duration)
        logger.warning(f"Request to {url} timed out: {e}")
        return {"success": False, "error": str(e)}

    except requests.exceptions.RequestException as e:
        duration = time.time() - start_time
        REQUEST_DURATION.observe(duration)
        logger.error(f"Request to {url} failed with error: {e}")
        return {"success": False, "error": str(e)}


def request_loop():
    """Main loop that sends requests based on the configuration."""
    while True:
        config = load_config()

        api_url = config.get("api_url", "https://example.com/api")
        interval = config.get("interval_seconds", 30)
        failure_rate = config.get("failure_rate", 0)
        failure_modes = config.get("failure_modes", [])

        logger.info(f"Making request to {api_url} with {failure_rate}% failure rate")
        result = make_request(api_url, failure_rate, failure_modes)
        logger.info(f"Request result: {result}")

        # Sleep until next interval
        time.sleep(interval)


def main():
    """Start the metrics server and request loop."""
    try:
        # Start Prometheus HTTP server
        start_http_server(8001)
        logger.info("Started Prometheus metrics server on port 8001")

        # Start the request loop in a separate thread
        request_thread = threading.Thread(target=request_loop)
        request_thread.daemon = True
        request_thread.start()

        logger.info("Started request loop")

        # Keep the main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down requester")

    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
        raise


if __name__ == "__main__":
    main()

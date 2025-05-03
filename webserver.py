import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def load_config():
    """Load configuration from config.json or create default if it doesn't exist."""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        else:
            default_config = {
                "api_url": "https://example.com/api",
                "interval_seconds": 30,
                "failure_rate": 10,
                "failure_modes": ["timeout", "500"],
            }
            with open(CONFIG_PATH, "w") as f:
                json.dump(default_config, f, indent=4)
            return default_config
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {
            "api_url": "https://example.com/api",
            "interval_seconds": 30,
            "failure_rate": 10,
            "failure_modes": ["timeout", "500"],
        }


def save_config(config):
    """Save configuration to config.json."""
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving config: {e}")
        return False


def get_config():
    config = load_config()
    return {
        "api_url": os.getenv("API_URL") or config.get("api_url", "https://example.com/api"),
        "interval_seconds": int(os.getenv("REQUEST_INTERVAL") or config.get("interval_seconds", 30)),
        "failure_rate": int(os.getenv("FAILURE_RATE") or config.get("failure_rate", 10)),
        "failure_modes": os.getenv("FAILURE_MODES", "").split(",") if os.getenv("FAILURE_MODES") else config.get("failure_modes", ["timeout", "500"])
    }


@app.route("/")
def index():
    """Render the main page with the configuration form."""
    config = get_config()
    return render_template("index.html", config=config)


@app.route("/config", methods=["POST"])
def update_config():
    """Update the configuration based on form data."""
    try:
        # Extract form data
        api_url = request.form.get("api_url")
        interval_seconds = int(request.form.get("interval_seconds", 30))
        failure_rate = float(request.form.get("failure_rate", 0))

        # Handle multiple checkboxes for failure modes
        failure_modes = request.form.getlist("failure_modes")

        # Validate inputs
        if not api_url:
            return render_template(
                "index.html", error="API URL is required", config=get_config()
            )

        if interval_seconds < 1:
            return render_template(
                "index.html",
                error="Interval must be at least 1 second",
                config=get_config(),
            )

        if not 0 <= failure_rate <= 100:
            return render_template(
                "index.html",
                error="Failure rate must be between 0 and 100",
                config=get_config(),
            )

        if not failure_modes and failure_rate > 0:
            return render_template(
                "index.html",
                error="Select at least one failure mode if failure rate > 0",
                config=get_config(),
            )

        # Create new config
        new_config = {
            "api_url": api_url,
            "interval_seconds": interval_seconds,
            "failure_rate": failure_rate,
            "failure_modes": failure_modes,
        }

        # Save the config
        if save_config(new_config):
            logger.info(f"Configuration updated: {new_config}")
            return redirect(url_for("index", updated=True))
        else:
            return render_template(
                "index.html", error="Failed to save configuration", config=get_config()
            )

    except Exception as e:
        logger.error(f"Error updating config: {e}")
        return render_template("index.html", error=str(e), config=get_config())


@app.route("/status")
def status():
    """Show the current configuration and recent request results."""
    config = get_config()
    # In a more complete implementation, we would also show recent request results
    return jsonify(
        {
            "config": config,
            "status": "running",  # This would be fetched from the requester in a real implementation
        }
    )


if __name__ == "__main__":
    # Ensure config exists
    load_config()
    app.run(host="0.0.0.0", port=5000, debug=True)

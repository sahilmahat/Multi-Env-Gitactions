from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)

# environment variable
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


@app.route("/")
def home():
    return f"""
    <h1>CI/CD Multi Environment Demo</h1>
    <p>Environment: {ENVIRONMENT}</p>
    <p>Time: {datetime.now()}</p>
    """


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "environment": ENVIRONMENT
    }


@app.route("/version")
def version():
    return {
        "version": os.getenv("VERSION", "1.0"),
        "environment": ENVIRONMENT
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

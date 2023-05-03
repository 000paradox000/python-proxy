import logging
import os
from pathlib import Path

import dotenv
import requests

from flask import Flask
from flask import jsonify
from flask import request

dotenv.load_dotenv()

logging.basicConfig(level=logging.DEBUG)

base_dir = Path(__file__).resolve().parent

app = Flask(__name__)


@app.route("/<path:request_path>", methods=["GET", "POST"])
def index(request_path):
    query_string = request.query_string.decode("utf-8")
    query_string_dict = dict(request.args)

    real_url = os.environ["REAL_URL"]

    logging.info(f"Request path: {request_path}")
    logging.info(f"Query String: {query_string}")

    url = real_url + "/" + request_path

    kwargs = {
        "url": url,
        "params": query_string_dict,
    }
    response = requests.get(**kwargs)

    return response.json()


@app.route("/openai/<path:request_path>", methods=["GET", "POST"])
def openai_proxy(request_path):
    query_string = request.query_string.decode("utf-8")
    query_string_dict = dict(request.args)

    openai_api_key = os.environ["OPENAI_API_KEY"]
    openai_real_url = os.environ["OPENAI_REAL_URL"]

    logging.info(f"Request path: {request_path}")
    logging.info(f"Query String: {query_string}")

    url = openai_real_url + "/" + request_path
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }

    request_data = request.get_json()

    data = {
        "prompt": request_data["prompt"],
    }
    data.update(request_data["llm_settings"])

    kwargs = {
        "url": url,
        "params": query_string_dict,
        "headers": headers,
        "json": data,
    }
    response = requests.post(**kwargs)

    return response.json()


def main():
    """Run the flask application if the main module is invoked directly."""
    print("Running from main")
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )


if __name__ == "__main__":
    main()

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

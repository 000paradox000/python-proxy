from pathlib import Path

import dotenv

from flask import Flask
from flask import request

dotenv.load_dotenv()

base_dir = Path(__file__).resolve().parent

app = Flask(__name__)


@app.route("/<path:url>", methods=["GET", "POST"])
def index():
    header = request.headers.get("referer")
    if not referer:
        return Response(
            "Relative URL sent without a a proxying request referal. Please specify a valid proxy host (/p/url)",
            400,
        )
    proxy_ref = proxied_request_info(referer)
    host = proxy_ref[0]
    redirect_url = "/p/%s/%s%s" % (
        host,
        url,
        (
            "?" + request.query_string.decode("utf-8")
            if request.query_string
            else ""
        ),
    )
    LOG.debug("Redirecting relative path to one under proxy: %s", redirect_url)
    return redirect(redirect_url)

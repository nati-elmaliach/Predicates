# server.py
import hashlib
import json
import random
import time
from typing import Any, Dict

from data import test_predicates
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


def generate_etag(data: Dict[str, Any]) -> str:
    """Generate an ETag from the data using a hash function."""
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()


@app.route("/api/v1/predicate", methods=["GET"])
def get_predicate():
    # Generate a random predicate
    predicate = random.choice(test_predicates)

    # Generate ETag for this predicate
    etag = generate_etag(predicate)

    # Check If-None-Match header
    if_none_match = request.headers.get("If-None-Match")
    if if_none_match and if_none_match == etag:
        # Return 304 Not Modified if ETag matches
        return "", 304

    # Create response with ETag
    response = make_response(jsonify(predicate))
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "no-cache"  # Ensure client always checks ETag
    return response


def run_server():
    print("\nStarting server test...")
    # Run the Flask app
    from threading import Thread

    server = Thread(target=app.run, kwargs={"debug": False})
    server.start()

    # Wait for server to start
    time.sleep(2)

    print("\nServer is running. Press Ctrl+C to stop.")

"""Flask entry point. All data structures and algorithms live in /dsa."""

import os
import secrets
from threading import RLock

from flask import Flask, render_template

from dsa.graph_utils import load_sample
from routes.graph_routes import pages


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=secrets.token_hex(32), MAX_CONTENT_LENGTH=16 * 1024)
    if test_config:
        app.config.update(test_config)
    app.extensions["campus_graph"] = load_sample()
    app.extensions["graph_lock"] = RLock()
    app.register_blueprint(pages)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("error.html", title="Page not found", code=404,
                               message="That path isn't on this campus. Let's head back."), 404

    @app.errorhandler(413)
    def too_large(error):
        return render_template("error.html", title="Form too large", code=413,
                               message="Please submit a smaller form."), 413

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)

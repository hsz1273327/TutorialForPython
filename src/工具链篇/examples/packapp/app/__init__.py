from flask import Flask
from .api import restapi


def main() -> None:
    app = Flask("packapp")
    app.config["JSON_AS_ASCII"] = False
    restapi.init_app(app)
    app.run()

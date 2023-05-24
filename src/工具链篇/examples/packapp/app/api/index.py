from flask.json import jsonify
from flask.views import MethodView
from flask import Response
from .core import restapi


@restapi.register("/")
class IndexAPI(MethodView):

    def get(self) -> Response:
        result = {
            "description": "test api"
        }
        return jsonify(result)


__all__ = ["IndexAPI"]

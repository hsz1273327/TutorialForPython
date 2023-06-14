from flask import Blueprint, Flask
from flask.views import MethodView
from typing import Callable, Type, Optional


class APIView:
    def __init__(self, name: str = 'restapi', url_prefix: str = "/api", app: Optional[Flask] = None) -> None:
        self.restapi = Blueprint(name, __name__, url_prefix=url_prefix)
        if app:
            self.init_app(app)

    def register(self, url: str) -> Callable[[Type[MethodView]], Type[MethodView]]:
        def wrap(clz: Type[MethodView]) -> Type[MethodView]:
            self.restapi.add_url_rule(url, view_func=clz.as_view(clz.__name__))
            return clz
        return wrap

    def init_app(self, app: Flask) -> None:
        app.register_blueprint(self.restapi)


restapi = APIView()
__all__ = ["restapi", "APIView"]

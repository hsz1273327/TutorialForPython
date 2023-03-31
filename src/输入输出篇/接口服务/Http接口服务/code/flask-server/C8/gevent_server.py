from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from app import app
import logging
#werkzeug_log = logging.getLogger("werkzeug")
http_server = WSGIServer(('', 5000), app, log=logging.getLogger("werkzeug"))
http_server.serve_forever()

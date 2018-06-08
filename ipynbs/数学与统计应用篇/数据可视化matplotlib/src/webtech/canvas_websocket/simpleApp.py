#coding:utf-8

from gevent import monkey
monkey.patch_all()
from flask import Flask, make_response,request
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource
from werkzeug.debug import DebuggedApplication

from matplotlib.backends.backend_webagg_core import (
    FigureManagerWebAgg, new_figure_manager_given_figure)
from matplotlib.figure import Figure

import numpy as np
import io
import json
from purl import URL


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


html_content = """
<html>
  <head>
    <!-- TODO: There should be a way to include all of the required javascript
               and CSS so matplotlib can add to the set in the future if it
               needs to. -->
    <link rel="stylesheet" href="_static/css/page.css" type="text/css">
    <link rel="stylesheet" href="_static/css/boilerplate.css" type="text/css" />
    <link rel="stylesheet" href="_static/css/fbm.css" type="text/css" />
    <link rel="stylesheet" href="_static/jquery/css/themes/base/jquery-ui.min.css" >
    <script src="_static/jquery/js/jquery-1.11.3.min.js"></script>
    <script src="_static/jquery/js/jquery-ui.min.js"></script>
    <script src="mpl.js"></script>
    <script>
      /* This is a callback that is called when the user saves
         (downloads) a file.  Its purpose is really to map from a
         figure and file format to a url in the application. */
      function ondownload(figure, format) {
        window.open('download.' + format, '_blank');
      };
      $(document).ready(
        function() {
          /* It is up to the application to provide a websocket that the figure
             will use to communicate to the server.  This websocket object can
             also be a "fake" websocket that underneath multiplexes messages
             from multiple figures, if necessary. */
          var websocket_type = mpl.get_websocket_type();
          var websocket = new websocket_type("%(ws_uri)sws");
          // mpl.figure creates a new figure on the webpage.
          var fig = new mpl.figure(
              // A unique numeric identifier for the figure
              %(fig_id)s,
              // A websocket object (or something that behaves like one)
              websocket,
              // A function called when a file type is selected for download
              ondownload,
              // The HTML element in which to place the figure
              $('div#figure'));
        }
      );
    </script>
    <title>matplotlib</title>
  </head>
  <body>
    <div id="figure">
    </div>
  </body>
</html>
"""
def create_figure():
    """
    Creates a simple example figure.
    """
    fig = Figure()
    a = fig.add_subplot(111)
    t = np.arange(0.0, 3.0, 0.01)
    s = np.sin(2 * np.pi * t)
    a.plot(t, s)
    return fig

figure = create_figure()
Manager=new_figure_manager_given_figure(
    id(figure), figure)

class WebSocket_App(WebSocketApplication):
    """
    A websocket for interactive communication between the plot in
    the browser and the server.
    In addition to the methods required by tornado, it is required to
    have two callback methods:
        - ``send_json(json_content)`` is called by matplotlib when
          it needs to send json to the browser.  `json_content` is
          a JSON tree (Python dictionary), and it is the responsibility
          of this implementation to encode it as a string to send over
          the socket.
        - ``send_binary(blob)`` is called to send binary image data
          to the browser.
    """
    supports_binary = True

    def on_open(self):
        # Register the websocket with the FigureManager.
        print "open"
        manager = Manager
        manager.add_web_socket(self)
        if hasattr(self, 'set_nodelay'):
            self.set_nodelay(True)

    def on_close(self):
        # When the socket is closed, deregister the websocket with
        # the FigureManager.
        print "close"
        manager = Manager
        manager.remove_web_socket(self)

    def on_message(self, message):
        # The 'supports_binary' message is relevant to the
        # websocket itself.  The other messages get passed along
        # to matplotlib as-is.

        # Every message has a "type" and a "figure_id".
        manager = Manager
        print manager.web_sockets
        if type(message) != str:
            print type(message)
        message = json.loads(message)
        if message['type'] == 'supports_binary':
            self.supports_binary = message['value']
        else:
            manager = Manager
            s = manager.handle_json(message)
            #print s

    def send_json(self, content):
        print "send_json"
        self.ws.send(json.dumps(content))
        #self.write_message(json.dumps(content))

    def send_binary(self, blob):
        print "send_binary"
        if self.supports_binary:
            self.ws.send(blob, binary=True)
            #self.write_message(blob, binary=True)
        else:
            data_uri = "data:image/png;base64,{0}".format(
                blob.encode('base64').replace('\n', ''))
            self.ws.send(data_uri)
            #self.write_message(data_uri)


@app.route('/')
def MainPage():
    manager = Manager
    ws_uri = "ws://{req}:7777/".format(req=URL(request.url).host())
    content = html_content % {"ws_uri": ws_uri, "fig_id": manager.num}
    return content

@app.route('/mpl.js')
def MplJs():
    """
    Serves the generated matplotlib javascript file.  The content
    is dynamically generated based on which toolbar functions the
    user has defined.  Call `FigureManagerWebAgg` to get its
    content.
    """
    js_content = FigureManagerWebAgg.get_javascript()
    resp = make_response(js_content, 200)
    resp.headers['Content-Type'] = 'application/javascript'
    return resp

@app.route('/download.<fmt>')
def download(fmt):
    """
    Handles downloading of the figure in various file formats.
    """
    manager = Manager

    mimetypes = {
        'ps': 'application/postscript',
        'eps': 'application/postscript',
        'pdf': 'application/pdf',
        'svg': 'image/svg+xml',
        'png': 'image/png',
        'jpeg': 'image/jpeg',
        'tif': 'image/tiff',
        'emf': 'application/emf'
    }

    buff = io.BytesIO()
    manager.canvas.print_figure(buff, format=fmt)

    resp = make_response(buff.getvalue(), 200)
    resp.headers['Content-Type'] = mimetypes.get(fmt, 'binary')
    return resp

if __name__ == '__main__':
    server = WebSocketServer(
    ('0.0.0.0', 7777),
    Resource([
        ('^/ws', WebSocket_App),
        ('^/.*', DebuggedApplication(app))
    ]),debug=False)
    print "started at 0.0.0.0:7777"
    server.serve_forever()

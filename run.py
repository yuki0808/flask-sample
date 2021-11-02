from flask import Flask
import logging
import logging.handlers
from pythonjsonlogger import jsonlogger
from ddtrace import patch_all; patch_all(logging=True)
from ddtrace import tracer

app = Flask(__name__)

handler = logging.handlers.RotatingFileHandler(
        '/var/log/log.txt',
        maxBytes=1024 * 1024)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
handler.setFormatter(formatter)
logging.basicConfig(format=formatter)
log = logging.getLogger(__name__)
log.level = logging.INFO
logging.getLogger().addHandler(handler)

@tracer.wrap()
@app.route('/')
def hello_world():
    log.info('Hello, World')
    return '<html><body><h1>Hello world!</h1></body></html>'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

import os
from fabric.api import local
from fabric.decorators import task


@task(alias='run')
def run_flask(port="5000"):
    host = '0.0.0.0' if os.environ.get('DOCKERIZED') else '127.0.0.1'
    local(f"FLASK_APP=app.py FLASK_DEBUG=1 python -m flask run --host={host} -p {port}")

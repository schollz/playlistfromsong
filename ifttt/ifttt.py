from distutils.spawn import find_executable
from subprocess import call

from flask import Flask
from flask import jsonify
app = Flask(__name__)

import logging
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger('server')

@app.route('/download/a/song/<path:path>')
def hello(path):
    logger.info(path)
    path = path.replace("download/a/song","")
    cmd = "python3 -m pip install --upgrade playlistfromsong"
    logger.info(cmd)
    call(cmd.split())
    songs = " ".join(path.replace("/"," ").split())
    playlistfromsong = find_executable("playlistfromsong")
    cmd = [playlistfromsong,"-s",songs,"-n","1"]
    logger.info(" ".join(cmd))
    call(cmd)
    return jsonify({'success':True})

if __name__ == "__main__":
    from waitress import serve
    serve(app, listen='*:5001')


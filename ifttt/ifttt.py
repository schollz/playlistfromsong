from distutils.spawn import find_executable
from subprocess import call
import logging
from flask import Flask
from flask import jsonify
app = Flask(__name__)

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('server')


@app.route('/download/a/song/<path:path>')
def hello(path):
    logger.info(path)
    path = path.replace("download/a/song", "")
    cmd = "python3 -m pip install --upgrade playlistfromsong"
    logger.info(cmd)
    call(cmd.split())
    songs = " ".join(path.replace("/", " ").split())
    playlistfromsong = find_executable("playlistfromsong")
    cmd = [playlistfromsong, "-s", songs, "-n", "1"]
    logger.info(" ".join(cmd))
    call(cmd)
    return jsonify({'success': True})


if __name__ == "__main__":
    from waitress import serve
    serve(app, listen='*:5001')

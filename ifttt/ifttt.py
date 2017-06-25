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

playlistfromsong = find_executable("playlistfromsong")


@app.route('/download/<n>/<song>')
def download(n, song):
    cmd = "python3 -m pip install --upgrade playlistfromsong"
    call(cmd.split())
    cmd = [playlistfromsong, "-s", song, "-n", n]
    logger.info(" ".join(cmd))
    call(cmd)
    return jsonify({'success': True})


if __name__ == "__main__":
    from waitress import serve
    serve(app, listen='*:5001')

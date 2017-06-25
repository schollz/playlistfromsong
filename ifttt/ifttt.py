from distutils.spawn import find_executable
from subprocess import call
import logging
from argparse import ArgumentParser

from flask import Flask
from flask import jsonify
from waitress import serve

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('server')

playlistfromsong = find_executable("playlistfromsong")
folder_to_save_data = "."


@app.route('/download/<n>/<song>')
def download(n, song):
    cmd = "python3 -m pip install --upgrade playlistfromsong"
    call(cmd.split())
    cmd = [playlistfromsong, "-s", song, "-n", n, "-f", folder_to_save_data]
    logger.info(" ".join(cmd))
    call(cmd)
    return jsonify({'success': True})


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--folder', help='folder to save data')
    args = parser.parse_args()
    if args.folder is not None:
        folder_to_save_data = args.folder
    print("Starting server, saving data to %s" % folder_to_save_data)
    serve(app, listen='*:5001')

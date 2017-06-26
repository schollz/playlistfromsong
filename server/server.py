from distutils.spawn import find_executable
from subprocess import call
import logging
from argparse import ArgumentParser
import fnmatch
import os
import re

from flask import Flask, jsonify, send_from_directory, render_template
from waitress import serve

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger('server')

playlistfromsong = find_executable("playlistfromsong")
folder_to_save_data = os.path.join("/home/zns/Music/music")

def get_songs():
    matches = []
    num = 0
    for root, dirnames, filenames in os.walk(folder_to_save_data):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            filename = os.path.join(root, filename).replace(folder_to_save_data+'/','')
            filename = filename.replace('.mp3','')
            songname = filename
            if songname[-12:-11] == "-":
                songname = songname[:-12]
            songname = re.sub(r"[\(\[].*?[\)\]]", "", songname).strip()
            num += 1
            matches.append({'file':filename,'name':songname,'id':num})
    return matches

@app.route('/download/<n>/<song>')
def download(n, song):
    cmd = "python3 -m pip install --upgrade playlistfromsong"
    call(cmd.split())
    cmd = [playlistfromsong, "-s", song, "-n", n, "-f", folder_to_save_data]
    logger.info(" ".join(cmd))
    call(cmd)
    return jsonify({'success': True})


@app.route('/play')
def play():
    return render_template('index.html', songs=get_songs(), url="http://localhost:5000")


@app.route('/assets/<path:path>')
def static_stuff(path):
    return send_from_directory('assets', path)

@app.route('/song/<path:path>')
def send_song(path):
    return send_from_directory(folder_to_save_data, path)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--folder', help='folder to save data')
    args = parser.parse_args()
    if args.folder is not None:
        folder_to_save_data = args.folder
    print("Starting server, saving data to %s" % folder_to_save_data)
    serve(app, listen='*:5001')

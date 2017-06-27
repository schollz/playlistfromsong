from distutils.spawn import find_executable
from os.path import realpath, abspath, join, dirname
from subprocess import call
import fnmatch
from os import chdir, walk, getcwd
import re

from flask import Flask, jsonify, send_from_directory, render_template, request
from waitress import serve

app = Flask(__name__)

playlistfromsong = find_executable("playlistfromsong")
folder_to_save_data = getcwd()
port_for_server = "5000"
SERVER_DEBUG = True



def get_songs():
    matches = []
    num = 0
    for root, dirnames, filenames in walk(folder_to_save_data):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            filename = join(root, filename).replace(
                folder_to_save_data, '')
            filename = filename.replace('.mp3', '')
            if filename[0] == "/":
                filename = filename[1:]
            songname = filename
            if songname[-12:-11] == "-":
                songname = songname[:-12]
            songname = re.sub(r"[\(\[].*?[\)\]]", "", songname).strip()
            num += 1
            matches.append({'file': filename, 'name': songname, 'id': num})
    return matches


@app.route('/download/<n>/<song>')
def download(n, song):
    cmd = "python3 -m pip install --upgrade playlistfromsong"
    call(cmd.split())
    cmd = [playlistfromsong, "-s", song, "-n", n, "-f", folder_to_save_data]
    call(cmd)
    return jsonify({'success': True})


@app.route('/playlistfromsong')
def playlistfromsong_route():
    song = request.args.get('song')
    n = request.args.get('n')
    download(n, song)
    return play()


@app.route('/')
def play():
    cwd = getcwd()
    chdir(dirname(realpath(__file__)))
    rendered_template = render_template('index.html', songs=get_songs())
    chdir(cwd)
    return rendered_template


@app.route('/assets/<path:path>')
def static_stuff(path):
    return send_from_directory('assets', path)


@app.route('/song/<path:path>')
def send_song(path):
    if SERVER_DEBUG:
        print("Getting %s / %s" % (folder_to_save_data, path))
    return send_from_directory(folder_to_save_data, path)


def run_server(f, port):
    global folder_to_save_data, port_for_server
    if f != None:
        folder_to_save_data = abspath(f)
    if port != None:
        port_for_server = port
    print("\n\nStarting server, saving data to %s" % folder_to_save_data)
    serve(app, listen='*:' + port_for_server)

# -*- coding: utf-8 -*-

"""Console script for playlistfromsong."""

import click
from sys import exit
from os import getcwd

# For running as package
try:
	from .playlistfromsong import run, getTopFromLastFM
	from .server import run_server
except:
	from playlistfromsong import run, getTopFromLastFM
	from server import run_server

from sys import version_info

# # For running as script
# from playlistfromsong import run
# from server import run_server


@click.command()
@click.option('--num', '-n', default=3, help='Number of songs.')
@click.option('--song', '-s', default=None, help='Artist + Song to seed.')
@click.option('--bearer', '-b', default=None, help='Bearer token for Spotify.')
@click.option('--folder', '-f', default=None, help='Folder to save files.')
@click.option('--serve', is_flag=True, help='Start personal web server.')
@click.option('--port', default="5000", help='Internal port to run server (e.g. 5000).')
def main(num, song, bearer, folder, serve, port):
    """Console script for playlistfromsong."""
    if folder is None:
        folder = getcwd()
    if serve:
        run_server(folder, port)
    elif song != None:
        while True:
            song = getTopFromLastFM(song)
            if (version_info > (3, 0)):
                getinput = input
            else:
                getinput = raw_input
            c = getinput('Did you mean "' +
                         song + '"? (y/n) ')
            if c is "y":
                click.echo(
                    "Generating playlist for %d songs from '%s' \n(for generating more songs, use -n NUMBER)" % (num, song))
                run(song.replace(" - ", " "), num, bearer=bearer, folder=folder)
                break
            song = getinput(
                "Please enter the artist and song (e.g. The Beatles Let It Be): ")
    else:
        click.echo("Specify a song with --song 'The Beatles Let It Be'")


if __name__ == "__main__":
    main()

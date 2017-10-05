# -*- coding: utf-8 -*-

"""Console script for playlistfromsong."""

import click
from sys import exit
from os import getcwd
# import package future
from builtins import input

# For running as package
from playlistfromsong import run, getTopFromLastFM
from server import run_server


# # For running as script
# from playlistfromsong import run
# from server import run_server

@click.command()
@click.option('--num','-n', default=3, help='Number of songs.')
@click.option('--song','-s', default=None, help='Artist + Song to seed.')
@click.option('--bearer','-b', default=None, help='Bearer token for Spotify.')
@click.option('--folder','-f', default=None, help='Folder to save files.')
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
            recommendation_artist_song = getTopFromLastFM(song)
            c = input("Did you mean \"%s\"? (y/n)\n" % (recommendation_artist_song))
            if c is "y":
                num = 1
                song = recommendation_artist_song
                click.echo("Generating playlist for %d songs from '%s'" % (num, song))
                run(song.replace(" - ", " "), num, bearer=bearer, folder=folder)
                break
            song = input("Please enter the artist and song (e.g. The Beatles Let It Be): ")
    else:
        click.echo("Specify a song with --song 'The Beatles Let It Be'")
        
if __name__ == "__main__":
    main()

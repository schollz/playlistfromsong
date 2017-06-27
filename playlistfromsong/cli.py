# -*- coding: utf-8 -*-

"""Console script for playlistfromsong."""

import click
from sys import exit

from .playlistfromsong import run

@click.command()
@click.option('--num','-n', default=1, help='Number of songs.')
@click.option('--song','-s', default=None, help='Artist + Song to seed.')
@click.option('--bearer','-b', default=None, help='Bearer token for Spotify.')
@click.option('--folder','-f', default=None, help='Folder to save files.')
def main(num, song, bearer, folder):
    """Console script for playlistfromsong."""
    click.echo("Generating playlist for %d songs from '%s'" % (num, song))
    run(song, num, bearer, folder)

if __name__ == "__main__":
    main()

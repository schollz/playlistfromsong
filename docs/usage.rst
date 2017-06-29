=====
Usage
=====

Generate a playlist from song
------------------------------

Download a playlist from a song by specifying the artist and the song::

    playlistfromsong -s 'Miles Davis Blue In Green'

By default, three songs are downloaded (the original song plus 2 that are similar), but you can change this with ``-n``::

    playlistfromsong -s 'Miles Davis Blue In Green' -n 30

By default, the similar songs are found using last.fm, but you can choose to use Spotify instead, by providing a bearer token. Obtain a bearer token by going to https://developer.spotify.com/web-api/console/get-track/ and click "Get OAUTH_TOKEN". Then apply your token:::

    playlistfromsong -s 'Miles Davis Blue In Green' -n 30 -b 'TOKEN'


Finally, you can specify a specific place to store the files by using the ``-f`` flag::

    playlistfromsong -s 'Miles Davis Blue In Green' -f /music


Simple music server
--------------------

There is a built-in simple music server that you can use to play your music, but also includes an API for webhooks for automatically generating playlists from songs.

Star the server using::

    playlistfromsong --serve -f /path/to/music

The default port is 5000, and you should be able to see your server at http://localhost:5000. You can also specify the port with ``--port X``. 

There are routes for directly downloading songs. For instance, to generate a playlist in the current folder, just open::

    http://localhost:5000/download/10/Miles Davis Blue In Green

This is very effective for using with IFTTT to automatically download playlists based on songs that are liked on Youtube / Spotify.



================
playlistfromsong
================


.. image:: https://img.shields.io/pypi/v/playlistfromsong.svg
        :target: https://pypi.python.org/pypi/playlistfromsong

.. image:: https://img.shields.io/travis/schollz/playlistfromsong.svg
        :target: https://travis-ci.org/schollz/playlistfromsong

.. image:: https://readthedocs.org/projects/playlistfromsong/badge/?version=latest
        :target: https://playlistfromsong.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/schollz/playlistfromsong/shield.svg
     :target: https://pyup.io/repos/github/schollz/playlistfromsong/
     :alt: Updates


Generate an offline playlist from a single song.

Features
---------

- Similar song matching using last.fm or Spotify
- Automatic downloading of songs
- Builtin music server for webhooks

Quickstart
------------

Install with ``pip``::
    
    pip install playlistfromsong


Download a playlist of 5 songs similar to Miles Davis' *Blue In Green*::

    playlistfromsong --song 'Miles Davis Blue In Green' --num 5 -f /path/to/save

.. image:: http://i.imgur.com/ldVHZcc.gif
     :target: http://i.imgur.com/ldVHZcc.gif
     :alt: Demo1

Use a bearer token ``--bearer`` to use Spotify to find suggestions::

    playlistfromsong --song 'Miles Davis Blue In Green' --num 5 -f /path/to/save -b 'BEARER'

.. image:: http://i.imgur.com/uzEEEFh.gif
     :target: http://i.imgur.com/uzEEEFh.gif
     :alt: Demo1


For more complete usage, see the docs.
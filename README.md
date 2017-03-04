# playlistfromsong

Generate a Pandora-like offline music station from a single song. The files are saved on your computer so you can play them as much as you want.

*playlistfromsong* uses a single song as a seed. The respective song is found on last.fm and song suggestions extracted. The song audio is then downloaded from the respective Youtube video.

# Install

[Download lxml](http://lxml.de/installation.html) and [download ffmpeg](https://ffmpeg.org/download.html).

Then, to install with

```
pip install playlistfromsong
```
    
# Run

```bash
playlistfromsong --song 'The Beatles Let It Be'
```


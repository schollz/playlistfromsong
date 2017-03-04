# playlistfromsong

Generate a Pandora-like offline music station from a single song. The files are saved on your computer so you can play them as much as you want.

You supply a single song. *playlistfromsong* thgen finds the song on last.fm and extracts the song suggestions. Then song audio is downloaded from the respective Youtube video for each song suggestion.

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


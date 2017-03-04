# playlistfromsong

Generate a Pandora-like offline music station from a single song. The files are saved on your computer so you can play them as much as you want.

You supply a single song and *playlistfromsong* goes to the respective song page on last.fm and extracts the song suggestions. You can also provide a bearer token (`--bearer`) to use Spotify instead of last.fm. Then song audio is downloaded from the respective Youtube video for each song suggestion. 

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

![](http://i.imgur.com/Yp0EdJq.gif)

You can also use Spotify if you provide a Bearer token (which [you can get here](https://developer.spotify.com/web-api/console/get-track/)):

![](http://i.imgur.com/PEKuind.gif)

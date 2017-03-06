# playlistfromsong

[![Build Status](https://travis-ci.org/schollz/playlistfromsong.svg?branch=master)](https://travis-ci.org/schollz/playlistfromsong)

Generate a Pandora-like offline music station from a single song. The files are saved on your computer so you can play them as much as you want.

You supply a single song and *playlistfromsong* goes to the respective song page on last.fm and extracts the song suggestions.
You can also provide a bearer token (`--bearer` or use program config) to use Spotify instead of last.fm.
Then song audio is downloaded from the respective Youtube video for each song suggestion. 

# Dependencies 

### [lxml](http://lxml.de/installation.html)
```
STATIC_DEPS=true pip install lxml
```

### [ffmpeg](https://ffmpeg.org/download.html)

#### Mac
```
brew install ffmpeg
```

#### Ubuntu
```
sudo apt-get install ffmpeg
```

#### Windows
[Download](https://ffmpeg.org/download.html)

# Install

```
pip install playlistfromsong
```
    
# Run

```bash
playlistfromsong --song 'Miles Davis Blue In Green'
```

![](http://i.imgur.com/ldVHZcc.gif)

You can also use Spotify if you provide a Bearer token (which [you can get here](https://developer.spotify.com/web-api/console/get-track/)):

![](http://i.imgur.com/uzEEEFh.gif)

You can also set the spotify bearer token

```
playlistfromsong config --open
```

That command will open the config file with default application.

Edit the config file and add following entry 

    spotify_bearer_token: <your spotify bearer token>

change `<your spotify bearer token>` with actual token and save.

After editing the config file, everytime you use the program that token will be loaded.

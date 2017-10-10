# -*- coding: utf-8 -*-

"""Main module."""
"""Main script for playlistfromsong.py, cf.
https://github.com/schollz/playlistfromsong/
"""
from sys import exit, platform, stderr, version_info
from os.path import join, isfile, abspath
from os import chdir, mkdir
from appdirs import user_data_dir
from subprocess import Popen, PIPE
import multiprocessing
import argparse
import json
import urllib

import appdirs
from requests import get
import yaml
from youtube_dl import YoutubeDL
from bs4 import BeautifulSoup

try:
    output = Popen(
        ['ffmpeg', '--help'],
        stdout=PIPE,
        stderr=PIPE
    )
except:
    print("Need to install ffmpeg (https://ffmpeg.org/download.html)")
    exit(-1)

programSuffix = ""
if platform.startswith('win'):
    programSuffix = ".exe"

"""Check python version
"""
pyVersion = version_info[0]

"""For available codec run following commands

    ffmpeg -codec
"""
FFMPEGDefaultCodec = 'mp3'
FFMPEGDefaultQuality = '192'
defaultConfigFile = join(
    user_data_dir(
        'playlistfromsong',
        'schollz'),
    'playlistfromsong.yaml')
defautlConfigValue = {
    'spotify_bearer_token': None,
    'ffmpeg_codec': FFMPEGDefaultCodec,
    'ffmpeg_quality': FFMPEGDefaultQuality,
}

DEBUG = False


def getYoutubeURLFromSearch(searchString):
    if pyVersion < 3:
        urlParse = urllib.quote_plus(searchString)
    else:
        urlParse = urllib.parse.quote_plus(searchString)
    urlToGet = "https://www.youtube.com/results?search_query=" + urlParse  # NOQA
    r = get(urlToGet)
    soup = BeautifulSoup(r.content, 'html.parser')
    videos = soup.find_all('h3', class_='yt-lockup-title')
    for video in videos:
        link = video.find_all('a')[0]
        url = "https://www.youtube.com" + link.get('href')
        if 'googleads' in url:
            continue
        title = link.text
        if 'doubleclick' in title:
            continue
        if 'list=' in url:
            continue
        if 'album review' in title.lower():
            continue
        return url
    return ""


def getCodecAndQuality(codec=None, quality=None):
    """Get preferred codec and quality.

    This function determine which codec and quality to use,
    depend on program config, user setting and hardcoded default.

    Args:
        codec: Codec from user
        quality: preferred quality from user

    Returns:
        Tuple of (codec, preferredQuality)

    """
    if codec is not None and quality is not None:
        return codec, quality

    # copy the default value
    defaultCodec = FFMPEGDefaultCodec
    defaultQuality = FFMPEGDefaultQuality

    # # load from default config file
    # try:
    #     configValue = loadConfig(configFilePath=defaultConfigFile)
    #     defaultCodec = configValue.get('ffmpeg_codec', FFMPEGDefaultCodec)
    #     defaultQuality = configValue.get(
    #         'ffmpeg_quality', FFMPEGDefaultQuality)
    # except Exception as e:  # pragma: no cover
    #     print('{}:{}'.format(type(e), e))
    #     print("Can't load codec and quality from config file.")

    codec = defaultCodec if codec is None else codec
    quality = defaultQuality if quality is None else quality

    return codec, quality


def downloadURL(url, preferredCodec=None, preferredQuality=None):
    """ Downloads song using youtube_dl and the song's youtube
    url.
    """
    codec, quality = getCodecAndQuality()

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec,
            'preferredquality': quality,
        },
            {'key': 'FFmpegMetadata'},
        ],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)
    except:
        print("Problem downloading " + url)
    return None


def getYoutubeAndRelatedLastFMTracks(lastfmURL):
    """find the YouTube URL for the last.fm URL and get the next recommendations

    Args:
        lastfmURL: the last.fm URL of the song

    Returns:
        tuple of YouTube URL for the current song and a
        list of the next recomendations
    """
    try:
        artistName = lastfmURL.split('/')[4].replace('+', ' ')
        songName = lastfmURL.split('/')[-1].replace('+', ' ')
    except:
        return "", []
    print('%s - %s' % (artistName, songName))
    youtubeURL = ""
    lastfmTracks = []

    r = get(lastfmURL)
    soup = BeautifulSoup(r.content, 'html.parser')

    try:
        link = soup.find_all('div', class_='video-preview')
        youtubeURL = link[0].find_all('a')[0].get('href')
    except:
        youtubeURL = getYoutubeURLFromSearch(
            '%s - %s official' % (artistName, songName))

    try:
        sections = soup.find_all(
            "section", class_="grid-items-section")[0].find_all('a')
        for track in sections:
            lastfmTracks.append('https://www.last.fm' + track.get('href'))
    except:
        youtubeURL = getYoutubeURLFromSearch(
            '%s - %s official' % (artistName, songName))

    lastfmTracks = list(set(lastfmTracks))
    return (youtubeURL, lastfmTracks)


def useLastFM(song, num):
    """get recommendations from last.fm and find links on YouTube

    Args:
        song: the artist + song to search for on Spotify
        num: number of songs to recommend (1-100)

    Returns:
        list of YouTube URLs that are recommended from last.fm
    """
    searchTrack = song
    r = get('https://www.last.fm/search?q=%s' %
            searchTrack.replace(' ', '+'))
    soup = BeautifulSoup(r.content, 'html.parser')
    firstURL = ""
    try:
        chartlist = soup.find_all('table', class_='chartlist')[0]
    except:
        return []
    for link in chartlist.find_all('a', class_='link-block-target'):
        firstURL = 'https://www.last.fm' + link.get('href')
        break

    youtubeLinks = []
    print("\nPLAYLIST: \n")
    data = getYoutubeAndRelatedLastFMTracks(firstURL)
    finishedLastFMTracks = [firstURL]
    youtubeLinks.append(data[0])
    lastfmTracksNext = data[1]

    tries = 0
    while len(youtubeLinks) < num:
        lastfmTracks = list(set(lastfmTracksNext) - set(finishedLastFMTracks))
        p = multiprocessing.Pool(multiprocessing.cpu_count())
        lastfmTracksNext = []
        for data in p.map(getYoutubeAndRelatedLastFMTracks, lastfmTracks):
            if len(data[0]) > 0:
                youtubeLinks.append(data[0])
                lastfmTracksNext += data[1]
            if len(youtubeLinks) >= num:
                break
        finishedLastFMTracks += lastfmTracks
        tries += 1
        if tries > 5:
            break

    return youtubeLinks


def useSpotify(song, num, bearer):
    """get recommendations from Spotify and find links on YouTube

    Args:
        song: the artist + song to search for on Spotify
        num: number of songs to recommend (1-100)
        bearer: bearer token

    Returns:
        list of YouTube URLs that are recommended from Spotify
    """
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + bearer,
    }
    r = get('https://api.spotify.com/v1/search?q=%s&type=track,artist' % song.replace(' ', '+'), headers=headers)  # NOQA
    if r.status_code != 200:
        print(json.loads(r.text)['error']['message'])
        print("To get an autorization code, goto ")
        print("https://developer.spotify.com/web-api/console/get-track/")
        print("and click 'Get OAUTH TOKEN'")
        exit(-1)
    songJSON = json.loads(r.text)

    try:
        spotifyID = songJSON['tracks']['items'][0]['id']
        songName = songJSON['tracks']['items'][0]['name']
        artistName = songJSON['tracks']['items'][0]['artists'][0]['name']
        print("%s - %s (%s)" % (artistName, songName, spotifyID))
    except:
        return []
    r = get('https://api.spotify.com/v1/recommendations?seed_tracks=%s&limit=%d' % (spotifyID, num - 1), headers=headers)  # NOQA
    recommendationJSON = json.loads(r.text)
    linksToFindOnYoutube = []
    for track in recommendationJSON['tracks']:
        songName = track['name']
        artistName = track['artists'][0]['name']
        print("%s - %s" % (artistName, songName))
        linksToFindOnYoutube.append(
            "%s - %s official" % (artistName, songName))

    # Start downloading and print out progress
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    print("\nSearching YouTube for links...")
    urlsToDownload = []
    for i, link in enumerate(p.imap_unordered(
            getYoutubeURLFromSearch, linksToFindOnYoutube), 1):
        urlsToDownload.append(link)
        stderr.write(
            '\r...{0:2.1%} complete'.format(i / len(linksToFindOnYoutube)))
    print("")
    return urlsToDownload


def run(song, num, bearer=None, folder=None):
    if song is None:
        song = input(
            "Enter the artist and song (e.g. The Beatles Let It Be): ")

    youtubeLinks = []
    if num == 1:
        youtubeLinks.append(getYoutubeURLFromSearch(song))
    elif bearer is None:
        youtubeLinks = useLastFM(song, num)
    else:
        print("Using spotify")
        youtubeLinks = useSpotify(song, num, bearer)

    if len(youtubeLinks) == 0:
        print("Could not find song recommendations for '%s'" % song)
        return

    # Start downloading and print out progress
    if folder is not None:
        chdir(folder)
    else:
        folder = abspath('.')
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    print("\nStarting download...")
    for i, _ in enumerate(p.imap_unordered(downloadURL, youtubeLinks), 1):
        stderr.write(
            '\r...{0:2.1%} complete'.format(i / len(youtubeLinks)))

    print("\n\n%d tracks saved to %s\n" % (len(youtubeLinks), folder))
    return


def getTopFromLastFM(song):
    """ get top recommendation from last.fm

        Args:
            song: the artist + song to search for recommendation

        Returns:
            artist + song
    """
    searchTrack = song
    r = get('https://www.last.fm/search?q=%s' %
            searchTrack.replace(' ', '+'))
    soup = BeautifulSoup(r.content, 'html.parser')
    firstURL = ""
    try:
        chartlist = soup.find_all('table', class_='chartlist')[0]
    except:
        return []
    for link in chartlist.find_all('a', class_='link-block-target'):
        firstURL = link.get('href')
        break

    try:
        artistName = firstURL.split('/')[2].replace('+', ' ')
        songName = firstURL.split('/')[-1].replace('+', ' ')
    except:
        return "Could not find song recommendations for '%s'" % song
    return '%s - %s' % (artistName, songName)

#!/usr/bin/python3
import sys
import os
import multiprocessing

try:
    import requests
except:
    print("Need to install requests")
    print("python3 -m pip install requests")

try:
    import click
except:
    print("Need to install click")
    print("python3 -m pip install click")

try:
    from lxml import html
except:
    print("Need to install lxml")
    print("python3 -m pip install lxml")


programSuffix = ""


def downloadURL(url):
    if len(url) == 0:
        return
    os.system("youtube-dl%s -x --audio-quality 3 --audio-format mp3 %s" %
              (programSuffix, url))


def getYoutubeAndRelatedLastFMTracks(lastfmURL):
    print('Working on %s' % lastfmURL)
    youtubeURL = ""
    lastfmTracks = []

    r = requests.get(lastfmURL)
    tree = html.fromstring(r.content)
    youtubeSection = tree.xpath('//div[@class="video-preview"]')
    if len(youtubeSection) > 0:
        possibleYoutubes = youtubeSection[0].xpath('//a[@target="_blank"]')
        for possibleYoutube in possibleYoutubes:
            if 'href' in possibleYoutube.attrib:
                if 'youtube.com' in possibleYoutube.attrib['href']:
                    youtubeURL = possibleYoutube.attrib['href']
                    break

    sections = tree.xpath('//section[@class="grid-items-section"]')
    for track in sections[0].findall('.//a'):
        lastfmTracks.append('https://www.last.fm' + track.attrib['href'])

    lastfmTracks = list(set(lastfmTracks))
    return (youtubeURL, lastfmTracks)


@click.command()
@click.option('--song', prompt='Enter an artist and song name',
              help='The artist+song to seed playlist (e.g. "The Beatles Hey Jude")')
@click.option('--num', default=30, help='Max number of songs.')
def getTracks(song, num):
    """
    Download a playlist seeded from a single song.

    Make sure to have 

    youtube-dl (https://rg3.github.io/youtube-dl/)

    and 

    ffmpeg (https://ffmpeg.org/download.html)

    installed.
    """
    searchTrack = song
    r = requests.get('https://www.last.fm/search?q=%s' %
                     searchTrack.replace(' ', '+'))
    tree = html.fromstring(r.content)
    possibleTracks = tree.xpath('//span/a[@class="link-block-target"]')
    firstURL = ""
    for i, track in enumerate(possibleTracks):
        firstURL = 'https://www.last.fm' + track.attrib['href']
        break
    print(firstURL)

    youtubeLinks = []
    data = getYoutubeAndRelatedLastFMTracks(firstURL)
    finishedLastFMTracks = [firstURL]
    youtubeLinks.append(data[0])
    lastfmTracksNext = data[1]

    while len(youtubeLinks) < num:
        lastfmTracks = list(set(lastfmTracksNext)-set(finishedLastFMTracks))
        p = multiprocessing.Pool(multiprocessing.cpu_count())
        lastfmTracksNext = []
        for data in p.map(getYoutubeAndRelatedLastFMTracks, lastfmTracks):
            youtubeLinks.append(data[0])
            lastfmTracksNext += data[1]
        finishedLastFMTracks += lastfmTracks

    print(youtubeLinks)
    newDir = '-'.join(searchTrack.split())

    try:
        os.mkdir(newDir)
    except:
        pass
    os.chdir(newDir)
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    p.map(downloadURL, youtubeLinks)

    print("%d tracks saved to %s" % (len(youtubeLinks), newDir))

if __name__ == '__main__':
    is_windows = sys.platform.startswith('win')
    if is_windows:
        programSuffix = ".exe"
    getTracks()

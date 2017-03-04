import sys
import os
import subprocess
import multiprocessing
import argparse

import requests

try:
    from lxml import html
except:
    print("Need to install lxml")
    print("See http://lxml.de/installation.html")
    sys.exit(-1)

try:
    output = subprocess.Popen(
        ['ffmpeg', '--help'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
except:
    print("Need to install ffmpeg (https://ffmpeg.org/download.html)")
    sys.exit(-1)

programSuffix = ""


def downloadURL(url):
    command = "youtube-dl%s -x --audio-quality 3 --audio-format mp3 %s" % (
        programSuffix, url)
    if len(url) == 0:
        return
    output = subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    foo = output.stdout.read()
    # print("Downloaded %s" % url)


def getYoutubeAndRelatedLastFMTracks(lastfmURL):
    artistName = lastfmURL.split('/')[4].replace('+',' ')
    songName = lastfmURL.split('/')[-1].replace('+',' ')
    print('%s - %s' % (artistName,songName))
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


def main():
    parser = argparse.ArgumentParser(prog='playlistfromsong')
    parser.add_argument("-s", "--song", help="song to seed, e.g. 'The Beatles Let It Be'")
    parser.add_argument("-n", "--num", help="number of songs to download")
    args = parser.parse_args()

    num = 30
    try:
        num = int(args.num)
    except:
        pass

    if args.song == None:
        song = input(
            "Enter the artist and song (e.g. The Beatles Let It Be): ")
    else:
        song = args.song

    searchTrack = song
    r = requests.get('https://www.last.fm/search?q=%s' %
                     searchTrack.replace(' ', '+'))
    tree = html.fromstring(r.content)
    possibleTracks = tree.xpath('//span/a[@class="link-block-target"]')
    firstURL = ""
    for i, track in enumerate(possibleTracks):
        firstURL = 'https://www.last.fm' + track.attrib['href']
        break

    youtubeLinks = []
    print("\nPLAYLIST: \n")
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
            if len(youtubeLinks) >= num:
                break
        finishedLastFMTracks += lastfmTracks

    # print(youtubeLinks)
    newDir = '-'.join(searchTrack.split())


    try:
        os.mkdir(newDir)
    except:
        pass
    os.chdir(newDir)
    p = multiprocessing.Pool(multiprocessing.cpu_count())

    # Start downloading and print out progress
    print("\nStarting download...")
    for i, _ in enumerate(p.imap_unordered(downloadURL, youtubeLinks), 1):
        sys.stderr.write('\r...{0:%} complete'.format(i/len(youtubeLinks)))

    print("\n\n%d tracks saved to %s\n" % (len(youtubeLinks), newDir))

if __name__ == '__main__':
    is_windows = sys.platform.startswith('win')
    if is_windows:
        programSuffix = ".exe"
    main()

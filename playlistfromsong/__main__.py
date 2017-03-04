import sys
import os
import subprocess
import multiprocessing
import argparse

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
    print("Downloading %s" % url)
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


def main():
    parser = argparse.ArgumentParser(prog='playlistfromsong')
    parser.add_argument("-s", "--song", help="list available files")
    parser.add_argument("-n", "--num", help="don't add date")
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
    p.map(downloadURL, youtubeLinks)

    print("%d tracks saved to %s" % (len(youtubeLinks), newDir))

if __name__ == '__main__':
    is_windows = sys.platform.startswith('win')
    if is_windows:
        programSuffix = ".exe"
    main()

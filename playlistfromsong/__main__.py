import sys
import os
import subprocess
import multiprocessing
import argparse
import json
import urllib
import youtube_dl

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


def getYoutubeURLFromSearch(searchString):
    urlToGet = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(searchString)  # NOQA
    page = requests.get(urlToGet)
    tree = html.fromstring(page.content)
    videos = tree.xpath('//h3[@class="yt-lockup-title "]')
    for video in videos:
        videoData = video.xpath('./a[contains(@href, "/watch")]')
        if len(videoData) == 0:
            continue
        if 'title' not in videoData[0].attrib or 'href' not in videoData[0].attrib:
            continue
        title = videoData[0].attrib['title']
        url = "https://www.youtube.com" + videoData[0].attrib['href']
        if 'googleads' in url:
            continue
        # print("Found url '%s'" % url)
        try:
            timeText = video.xpath(
                './span[@class="accessible-description"]/text()')[0]
            minutes = int(timeText.split(':')[1].strip())
            if minutes > 12 or timeText.count(":") == 3:
                continue
        except:
            pass
        if 'doubleclick' in title or 'list=' in url or 'album review' in title.lower():
            continue
        # print("'%s' = '%s' @ %s " % (searchString, title, url))
        return url
    return ""


def downloadURL(url):
    """ Downloads song using youtube_dl and the song's youtube
    url.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
            {'key': 'FFmpegMetadata'},
        ],

    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)
    except:
        print("Problem downloading " + url)
    return None


def getYoutubeAndRelatedLastFMTracks(lastfmURL):
    artistName = lastfmURL.split('/')[4].replace('+', ' ')
    songName = lastfmURL.split('/')[-1].replace('+', ' ')
    print('%s - %s' % (artistName, songName))
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


def useLastFM(song, num):
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

    tries = 0
    while len(youtubeLinks) < num:
        lastfmTracks = list(set(lastfmTracksNext) - set(finishedLastFMTracks))
        p = multiprocessing.Pool(multiprocessing.cpu_count())
        lastfmTracksNext = []
        for data in p.map(getYoutubeAndRelatedLastFMTracks, lastfmTracks):
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
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + bearer,
    }
    r = requests.get('https://api.spotify.com/v1/search?q=%s&type=track,artist' % song.replace(' ', '+'), headers=headers)  # NOQA
    if r.status_code != 200:
        print(json.loads(r.text)['error']['message'])
        print("To get an autorization code, goto ")
        print("https://developer.spotify.com/web-api/console/get-track/")
        print("and click 'Get OAUTH TOKEN'")
        sys.exit(-1)
    songJSON = json.loads(r.text)

    spotifyID = songJSON['tracks']['items'][0]['id']
    songName = songJSON['tracks']['items'][0]['name']
    artistName = songJSON['tracks']['items'][0]['artists'][0]['name']
    print("%s - %s (%s)" % (artistName, songName, spotifyID))

    r = requests.get('https://api.spotify.com/v1/recommendations?seed_tracks=%s&limit=%d' % (spotifyID, num-1), headers=headers)  # NOQA
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
    print("\nSearching Youtube for links...")
    urlsToDownload = []
    for i, link in enumerate(p.imap_unordered(getYoutubeURLFromSearch, linksToFindOnYoutube), 1):
        urlsToDownload.append(link)
        sys.stderr.write(
            '\r...{0:%} complete'.format(i / len(linksToFindOnYoutube)))
    print("")
    return urlsToDownload


def main():
    parser = argparse.ArgumentParser(prog='playlistfromsong')
    parser.add_argument(
        "-s", "--song", help="song to seed, e.g. 'The Beatles Let It Be'")
    parser.add_argument("-n", "--num", help="number of songs to download")
    parser.add_argument("-b", "--bearer", help="bearer token for Spotify (see https://developer.spotify.com/web-api/console/get-track/)")  # NOQA
    args = parser.parse_args()

    num = 30
    try:
        num = int(args.num)
    except:
        pass

    if args.song is None:
        song = input(
            "Enter the artist and song (e.g. The Beatles Let It Be): ")
    else:
        song = args.song

    youtubeLinks = []
    if args.bearer is None:
        youtubeLinks = useLastFM(song, num)
    else:
        youtubeLinks = useSpotify(song, num, args.bearer)

    # Start downloading and print out progress
    newDir = '-'.join(song.split())
    try:
        os.mkdir(newDir)
    except:
        pass
    os.chdir(newDir)
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    print("\nStarting download...")
    for i, _ in enumerate(p.imap_unordered(downloadURL, youtubeLinks), 1):
        sys.stderr.write('\r...{0:%} complete'.format(i / len(youtubeLinks)))

    print("\n\n%d tracks saved to %s\n" % (len(youtubeLinks), newDir))


if __name__ == '__main__':
    is_windows = sys.platform.startswith('win')
    if is_windows:
        programSuffix = ".exe"
    main()

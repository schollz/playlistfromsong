"""test main module."""
from unittest import mock

import pytest

PATCH_MODULE = 'playlistfromsong.__main__'


@pytest.mark.parametrize('url', ['', 'https://www.youtube.com/watch?v=YSa5CO2cu-c'])
def test_download_url(url):
    """test func."""
    output = mock.Mock()
    with mock.patch(PATCH_MODULE + '.subprocess') as m_sp:
        m_sp.Popen.return_value = output
        from playlistfromsong import __main__
        # run
        f = __main__.downloadURL(url)

        # test
        if len(url) == 0:
            assert f is None
        else:
            assert f['alt_title'] == 'Take It or Leave It'


def test_get_youtube_and_related_lastfm_tracks():
    """test func."""
    tree = mock.Mock()
    response = mock.Mock()
    lastfm_url = (
        'https://www.last.fm/music/'
        'DragonForce/_/Dragon+Force+-+Through+The+Fire+And+Flames'
    )

    yt_section = mock.Mock()
    possible_yt = mock.Mock()
    possible_yt.attrib = {'href': 'https://www.youtube.com/watch?v=random_id'}
    yt_section.xpath.return_value = [possible_yt]
    lastfm_track = mock.Mock()
    lastfm_track.attrib = {'href': 'track_href'}
    lastfm_section = mock.Mock()
    lastfm_section.findall.return_value = [lastfm_track]
    tree.xpath.side_effect = [[yt_section], [lastfm_section]]

    youtube_url = possible_yt.attrib['href']
    lastfm_tracks = 'https://www.last.fm{}'.format(lastfm_track.attrib['href'])

    with mock.patch(PATCH_MODULE + '.html') as m_html, \
            mock.patch(PATCH_MODULE + '.requests', return_value=response):
        m_html.fromstring.return_value = tree
        from playlistfromsong import __main__
        # run
        res = __main__.getYoutubeAndRelatedLastFMTracks(lastfm_url)
        assert res == (youtube_url, [lastfm_tracks])

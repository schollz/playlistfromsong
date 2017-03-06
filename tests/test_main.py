"""test main module."""
from unittest import mock
from itertools import product
import argparse

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
            return
        else:
            assert 'Take It' in f['alt_title']


def test_get_youtube_and_related_lastfm_tracks():
    """test func."""
    tree = mock.Mock()
    response = mock.Mock()
    lastfm_url = (
        'https://www.last.fm/music/The+Beatles/_/Let+It+Be'
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
        assert res[0] == "https://www.youtube.com/watch?v=random_id"


def test_parse_args():
    """test func."""
    argv = []
    exp_res = {'num': None, 'song': None, 'subparserName': None, 'bearer': None}
    from playlistfromsong import __main__
    # run
    res = __main__.parseArgs(argv)
    assert vars(res) == exp_res


@pytest.mark.parametrize(
    'subparserName, print_path, open',
    product(
        ['random_subcommand', 'config'],
        [True, False],
        [True, False],
    )
)
def test_handle_config_subcommand(subparserName, print_path, open):
    """test func."""
    args = argparse.Namespace(subparserName=subparserName, print_path=print_path, open=open)
    configFile = mock.Mock()
    with mock.patch(PATCH_MODULE + '.openFile') as m_open_file:
        from playlistfromsong import __main__
        # run
        res = __main__.handleConfigSubcommand(args, configFile)
        if args.subparserName == 'config':
            assert res
            if args.open:
                m_open_file.assert_called_once_with(configFile)
        else:
            assert not res


@pytest.mark.parametrize('platform', ['random', 'linux2'])
def test_open_file(platform):
    """test func."""
    path = mock.Mock()
    with mock.patch(PATCH_MODULE + '.subprocess') as m_sp, \
            mock.patch(PATCH_MODULE + '.sys') as m_sys, \
            mock.patch(PATCH_MODULE + '.os') as m_os:
        m_sys.platform = platform
        from playlistfromsong import __main__
        __main__.openFile(path)
        if platform == 'linux2':
            m_sp.call.assert_called_once_with(['xdg-open', path])
        else:
            m_os.startfile.assert_called_once_with(path)

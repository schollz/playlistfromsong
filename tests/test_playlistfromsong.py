#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `playlistfromsong` package."""

import pytest

from click.testing import CliRunner
from os.path import isfile
from os import remove

from playlistfromsong import playlistfromsong
from playlistfromsong import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_mainfunctions(response):
    """Test the main functions from playlistfrom song"""
    assert playlistfromsong.getYoutubeURLFromSearch('Led Zepplin Stairway to Heaven') == "https://www.youtube.com/watch?v=IS6n2Hx9Ykk"
    assert playlistfromsong.getCodecAndQuality() == ('mp3', '192')
    # assert playlistfromsong.downloadURL("https://www.youtube.com/watch?v=IS6n2Hx9Ykk") != None
    # assert isfile('Led Zeppelin - Stairway To Heaven (NOT LIVE) (Perfect Audio)-IS6n2Hx9Ykk.mp3')
    # remove('Led Zeppelin - Stairway To Heaven (NOT LIVE) (Perfect Audio)-IS6n2Hx9Ykk.mp3')
    assert len(playlistfromsong.useLastFM("Led Zepplin Stairway to Heaven",3)) == 3

def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    # assert '--help  Show this message and exit.' in help_result.output

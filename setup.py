from setuptools import setup
setup(
  name = 'playlistfromsong',
  packages = ['playlistfromsong'], # this must be the same as the name above
  version = '0.2',
  description = 'An offline music station generator',
  author = 'Zack Scholl',
  author_email = 'hypercube.platforms@gmail.com',
  url = 'https://github.com/schollz/playlistfromsong', # use the URL to the github repo
  download_url = 'https://github.com/schollz/playlistfromsong/archive/v0.2.tar.gz', # I'll explain this in a second
  keywords = ['music', 'youtube', 'playlist'], # arbitrary keywords
  classifiers = [],
  install_requires=[
        "requests",
        "youtube_dl",
  ],
  entry_points={'console_scripts': 
        [
        'playlistfromsong = playlistfromsong.__main__:main', 
        ], 
  },
)
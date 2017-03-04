from setuptools import setup
setup(
  name = 'playlistfromsong',
  packages = ['playlistfromsong'], 
  version = '0.8',
  description = 'An offline music station generator',
  author = 'Zack Scholl',
  author_email = 'hypercube.platforms@gmail.com',
  url = 'https://github.com/schollz/playlistfromsong',
  download_url = 'https://github.com/schollz/playlistfromsong/archive/v0.8.tar.gz', 
  keywords = ['music', 'youtube', 'playlist'], 
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

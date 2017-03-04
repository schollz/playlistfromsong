from setuptools import setup

setup(
    name='playlistfromsong',
    packages=['playlistfromsong'],
    version='0.9',
    description='An offline music station generator',
    author='Zack Scholl',
    url='https://github.com/schollz/playlistfromsong',
    author_email='hypercube.platforms@gmail.com',
    download_url='https://github.com/schollz/playlistfromsong/archive/v0.9.tar.gz',
    keywords=['music', 'youtube', 'playlist'],
    classifiers=[],
    install_requires=[
          "requests",
          "youtube_dl",
    ],
    setup_requires=['pytest-runner==2.11.1'],
    tests_require=[
        'pytest-flake8==0.8.1',
        'pytest==3.0.6',
        'pytest-cov==2.4.0'

    ],
    entry_points={'console_scripts': [
          'playlistfromsong = playlistfromsong.__main__:main',
    ], },
)

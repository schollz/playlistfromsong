from setuptools import setup

setup(
    name='playlistfromsong',
    packages=['playlistfromsong'],
    version='1.1.1',
    description='An offline music station generator',
    author='schollz',
    url='https://github.com/schollz/playlistfromsong',
    author_email='hypercube.platforms@gmail.com',
    download_url='https://github.com/schollz/playlistfromsong/archive/v1.1.0.tar.gz',
    keywords=['music', 'youtube', 'playlist'],
    classifiers=[],
    install_requires=[
        "requests",
        "youtube_dl",
        'appdirs',
        'pyyaml',
        'beautifulsoup4',
        "flask",
        "waitress",
    ],
    setup_requires=['pytest-runner'],
    include_package_data=True,
    tests_require=[
        'pytest-flake8',
        'pytest',
        'pytest-cov'

    ],
    entry_points={'console_scripts': [
        'playlistfromsong = playlistfromsong.__main__:main',
    ], },
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    "requests",
    "youtube_dl",
    'appdirs',
    'pyyaml',
    'beautifulsoup4',
    "flask",
    "waitress",
]

setup_requirements = [
    # 'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    name='playlistfromsong',
    version='2.2.2',
    description="Generate an offline playlist from a single song",
    long_description=readme + '\n\n' + history,
    author="Zack",
    author_email='hypercube.platforms@gmail.com',
    url='https://github.com/schollz/playlistfromsong',
    packages=find_packages(include=['playlistfromsong']),
    entry_points={
        'console_scripts': [
            'playlistfromsong=playlistfromsong.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='playlistfromsong',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

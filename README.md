# playlistfromsong

Generate a Pandora-like offline music station from a single song

# Install

[Download lxml](http://lxml.de/installation.html) and [download ffmpeg](https://ffmpeg.org/download.html).

Then, to install with

```
pip install playlistfromsong
```
    
# Run

```bash
playlistfromsong --song 'The Beatles Let It Be'
```


# Packaging notes

```
# Generate a new tag
gitc commit -am "Version bump"
git tag -a vX.Y -m "Description"
git push origin --tags

# Setup ~/.pypirc according to http://peterdowns.com/posts/first-time-with-pypi.html

# Run this for the first time
python setup.py register -r pypi

# Run to update
python setup.py sdist upload -r pypi
```

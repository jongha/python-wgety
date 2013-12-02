# wget for Python
[![Build Status](https://travis-ci.org/jongha/python-wgety.png?branch=master)](https://travis-ci.org/jongha/python-wgety)

wget is a Python library for save as internet web page.

## Usage

### As a library

Copy wgety.py anywhere you want and create new file include below codes.

    from wgety.wgety import Wgety

    w = Wgety()
    w.execute(url='http://www.python.org', filename='python.html');

### From the command line

    usage wgety.py url filename

    $ wgety.py http://www.python.org python.html




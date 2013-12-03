# wget for Python
[![Build Status](https://travis-ci.org/jongha/python-wgety.png?branch=master)](https://travis-ci.org/jongha/python-wgety)

wgety is a Python library for save files or web pages.

## Usage

### Setup

    $ python ./setup.py install

### Test

    $ python ./run.py
    
### Using as a library

Copy wgety.py anywhere you want and create new file include below codes.

    from wgety.wgety import Wgety

    w = Wgety()
    w.execute(url='http://www.python.org', filename='python.html', absolute_link=True);
    w.execute(url='http://www.python.org/images/python-logo.gif');

### From the command line

    usage wgety.py url filename

    $ wgety.py http://www.python.org python.html




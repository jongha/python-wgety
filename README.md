# wget for Python
[![Build Status](https://travis-ci.org/jongha/python-wget.png?branch=master)](https://travis-ci.org/jongha/python-wget)

wget is a Python library for save as internet web page.

## Usage

### As a library

Copy wget.py anywhere you want and create new file include below codes.

     import src.wget

     g = src.wget.Wget()
     g.execute(url='http://www.python.org', filename='python.html');

### From the command line

    usage wget.py url filename

    $ wget.py http://www.python.org python.html




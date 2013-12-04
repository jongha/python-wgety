# wget for Python
[![Build Status](https://travis-ci.org/jongha/python-wgety.png?branch=master)](https://travis-ci.org/jongha/python-wgety)

wgety is a Python library for non-interactive download of files from the Web. It supports HTTP, HTTPS. It works like wget utility in Linux. It also supports RELATIVE link to ABSOLUTE link conversion.

## Usage

### Setup

    $ python ./setup.py install

### Test

    $ python ./run.py

### Using as a library

Copy wgety.py anywhere you want and create new file include below codes. If you need RELATIVE link to ABSOLUTE link conversion, set True absolute_link option.

    from wgety.wgety import Wgety

    w = Wgety()
    w.execute(url='http://www.python.org', filename='python.html', absolute_link=True); # html file download
    w.execute(url='http://www.python.org/images/python-logo.gif'); # binary file down
    w.execute(url='http://www.python.org/images/python-logo.gif', filename='logo.gif'); # save as 'logo.gif'

### From the command line

    usage: wgety.py [-h] [-a] url [filename]

    $ wgety.py http://www.python.org

    or with full options.

    $ wgety.py -a http://www.python.org python.html

## License

python-wgety is available under the terms of the MIT License.

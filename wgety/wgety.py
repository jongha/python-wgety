#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
import os
import re
import time

try: # python 3
    from urllib.parse import urlparse
    from http.client import HTTPConnection

except ImportError:
    from httplib import HTTPConnection
    from urlparse import urlparse

try:
    import argparse
except ImportError:
    from optparse import OptionParser

regex_map = {
    'ROOT': [
        ' (src|href)=(["\'])(/[^"\']*)',
        '^(src|href)=(["\'])(/[^"\']*)'
        ],
    'PARENT': [
        ' (src|href)=(["\'])\.\./([^"\']*)',
        '^(src|href)=(["\'])\.\./([^"\']*)'
        ],
    'CURRENT': [
        ' (src|href)=(["\'])\./([^"\']*)',
        '^(src|href)=(["\'])\./([^"\']*)'
        ' (src|href)=(["\'])([^"\']*)',
        '^(src|href)=(["\'])([^"\']*)'
        ]
}

except_startswith_links = ['#', 'http', 'mailto', 'javascript' ]

class FileProgress(object):
    def __init__(self, total):
        self.total = total is not None and float(total) or 0 # has not content-length
        return

    def open(self, filename, mode):
        return open(filename, mode)

    def write(self, fo, contents):
        fo.write(contents)

        if self.total > 0: # download percent
            sys.stdout.write('\r%d%%' % int(float(fo.tell())/self.total*100))

        else: # has not content-length, show bytes downloaded
            sys.stdout.write('\r%d bytes' % int(float(fo.tell())))

        sys.stdout.flush()

class Wgety(object):
    BUFFER_SIZE = 512

    def __init__(self):
        return

    def _wgety(self, url, filename):

        http = HTTPConnection(urlparse(url).netloc)
        http.request('GET', url, headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36' })

        response = http.getresponse()
        fp = FileProgress(response.getheader('Content-Length'))
        f = fp.open(filename, 'wb')

        data = response.read(self.BUFFER_SIZE)
        while data:
            try:
                fp.write(f, data)
                data = response.read(self.BUFFER_SIZE)
            except:
                break

        sys.stdout.write('\r')
        f.close();

    def _get_absolute_link(self, url, line):

        link_type = None
        url_parsed = urlparse(url)
        t_url = url_parsed.path[1:].split('/')
        host = url_parsed.scheme + '://' + url_parsed.netloc

        t_url.insert(0, host)
        line = self._find_replace(line, t_url, regex_map)
        return line

    def _find_replace(self, line, url_tokens, regex_map):

        def _root(obj):
            path = obj.group(3).startswith('/') and obj.group(3) or ('/' + obj.group(3))
            return ' ' + obj.group(1) + '=' + obj.group(2) + url_tokens[0] + path

        def _parent(obj):
            _tokens = list(url_tokens);
            for i in range(2): _tokens.pop()

            path = obj.group(3).startswith('/') and obj.group(3) or ('/' + obj.group(3))
            return ' ' + obj.group(1) + '=' + obj.group(2) + '/'.join(_tokens) + path

        def _current(obj):
            _tokens = list(url_tokens);
            for i in range(1): _tokens.pop()

            for links in except_startswith_links:
                if obj.group(3).startswith(links):
                    return obj.group(0)

            path = obj.group(3).startswith('/') and obj.group(3) or ('/' + obj.group(3))
            return ' ' + obj.group(1) + '=' + obj.group(2) + '/'.join(_tokens) + path

        for map in regex_map:
            for exp in regex_map[map]:
                if map == 'ROOT':
                    line = re.sub(exp, _root, line)

                elif map == 'PARENT':
                    line = re.sub(exp, _parent, line)

                if map == 'CURRENT':
                    line = re.sub(exp, _current, line)

        return line

    def _compile(self, url, src_filename, dst_filename, absolute_link=True):
        if os.path.exists(dst_filename):
            os.remove(dst_filename)

        if absolute_link:
            src = codecs.open(src_filename, 'rb', 'utf-8')
            dst = codecs.open(dst_filename, 'wb', 'utf-8')

            l = src.readline()
            while l:
                l = self._get_absolute_link(url, l.strip());
                if len(l): dst.write(l + '\n')
                l = src.readline()

            src.close()
            dst.close()
            os.remove(src_filename)

        else:
            os.rename(src_filename, dst_filename)

        return

    def execute(self, url, filename=None, absolute_link=None):

        if filename is None:
            filename = url.split('/')[-1]

        temp_filename = '.' + filename
        if not url.startswith('http'): url = 'http://' + url # if http, https not included

        print('Getting... ' + url)
        self._wgety(url, temp_filename)


        if absolute_link is None: # get absolute_link option
            if os.path.splitext(filename)[1].lower() in ('.html', '.htm'):
                absolute_link = True
            else:
                absolute_link = False

        print('Compiling... ' + filename)
        self._compile(url, temp_filename, filename, absolute_link=absolute_link)

        print('Done.')

if __name__ == '__main__':
    l_argv = len(sys.argv)
    parser = argparse.ArgumentParser(description='wgety for Python')
    parser.add_argument('url', metavar='url', nargs=1, help='Download target url')
    parser.add_argument('filename', metavar='filename', nargs='?', default=None, help='This option will save to the local filename.')
    parser.add_argument('-a', '--absolute', action='store_true', help='Change to absolute link.')
    args = parser.parse_args()

    if l_argv > 1:
        wgety = Wgety()
        wgety.execute(url=sys.argv[1], filename=args.filename, absolute_link=args.absolute);
    else:
        print(args.accumulate(args.integers))


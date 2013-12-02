#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
import os
import re
from httplib import HTTPConnection
from urlparse import urlparse
#from http.client import HTTPConnection # for 3.3

regex_map = {
    'ROOT': [' (src|href)=(["\'])(/[^"\']*)', '^(src|href)=(["\'])(/[^"\']*)'],
    'PARENT': [' (src|href)=(["\'])\.\.([^"\']*)', '^(src|href)=(["\'])\.\.([^"\']*)'],
    'CURRENT': [
        ' (src|href)=(["\'])\.([^"\']*)',
        '^(src|href)=(["\'])\.([^"\']*)',
        ' (src|href)=(["\'])([^"\']*)',
        '^(src|href)=(["\'])([^"\']*)'
        ]
}

except_startswith_links = ['#', 'http', 'mailto', 'javascript' ]

class Wget(object):
    def __init__(self):
        return
     
    def _wget(self, url, filename):
        http = HTTPConnection(urlparse(url).netloc)
        http.request('GET', url, headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36' })

        response = http.getresponse()
        f = open(filename, 'wb')
        
        try:
            f.write(response.read())
        except:
            raise
            
        finally:
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
        src = codecs.open(src_filename, 'r', 'utf-8')
        dst = codecs.open(dst_filename, 'w', 'utf-8')
        
        l = src.readline()
        while l:
            l = self._get_absolute_link(url, l.strip());
            if len(l): dst.write(l + '\n')
            l = src.readline()
            
        src.close()
        dst.close()
        os.remove(src_filename)
        return
        
    def execute(self, url, filename=None, absolute_link=True):
        if filename is None:
            filename = 'output.html'
        
        temp_filename = '.' + filename
        if not url.startswith('http'): url = 'http://' + url # if http, https not included
        
        print('getting... ' + url)
        self._wget(url, temp_filename)
        
        print('compiling... ' + filename)
        self._compile(url, temp_filename, filename, absolute_link=absolute_link)
        
if __name__ == '__main__':
    if len(sys.argv) > 1:
        wget = Wget()
        wget.execute(url=sys.argv[1]);
    else:
        print('Useage: wget.py url')


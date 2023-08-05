from itertools import cycle
import re
from urllib.request import urlopen
import logging
from random import SystemRandom

RE_PROXYLINE = re.compile(r'^([^:]+):(\d+)$')
RE_PROXYLINE_AUTH = re.compile(
    r'^([^:]+):(\d+):(.+?):(.+)$'
)
logger = logging.getLogger('crawler.proxylist')
randomizer = SystemRandom()


class Proxy(object):
    __slots__ = ('host', 'port', 'user', 'password', 'proxy_type')

    def __init__(
            self, host=None, port=None, user=None,
            password=None, proxy_type=None
        ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.proxy_type = proxy_type

    def address(self):
        return '%s:%s' % (self.host, self.port)

    def auth(self):
        if self.user:
            return '%s:%s' % (self.user, self.password)
        else:
            return None


class ProxyList(object):
    def __init__(
            self, proxy_type='http', close_connection=False,
            proxy_user=None, proxy_password=None
        ):
        """
        Args:
            close_connection: if `True` close connection to proxy server
            after request done
        """
        self._servers = []
        self._source = None
        self.proxy_type = proxy_type
        self.close_connection = close_connection
        self.proxy_user = proxy_user
        self.proxy_password = proxy_password

    @classmethod
    def create_from_source(cls, src_type, src, **kwargs):
        pl = ProxyList(**kwargs)
        pl.load_source(src_type, src)
        return pl

    def load_source(self, source_type, source):
        assert source_type in ('file', 'url', 'list'), \
            'Incorrect source type: %s' % source_type
        if source_type == 'file':
            self.load_file(source)
        elif source_type == 'url':
            self.load_url(source)
        elif source_type == 'list':
            self.load_list(source)

    def load_file(self, path):
        self._source = {
            'type': 'file',
            'location': path,
        }
        with open(path) as inp:
            self.load_from_rawdata(
                inp.read().splitlines()
            )
            
    def load_url(self, url):
        self._source = {
            'type': 'url',
            'location': url,
        }
        return self.load_from_rawdata(
            urlopen(url).read().decode('utf-8').splitlines()
        )

    def load_list(self, items):
        self._source = {
            'type': 'list',
            'location': None,
        }
        return self.load_from_rawdata(items)

    def load_from_rawdata(self, lines): 
        servers = []
        for line in lines:
            line = line.strip()
            match = RE_PROXYLINE.match(line)
            # By default use authorization
            # passed to ProxyList constructor
            # it is None by default
            user = self.proxy_user
            password = self.proxy_password
            if not match:
                match = RE_PROXYLINE_AUTH.match(line)
                if not match:
                    logger.error('Invalid proxy line: %s' % line)
                else:
                    # Override default user and proxy
                    # If auth data is provided by proxy line
                    host, port, user, password = match.groups()
            else:
                host, port = match.groups()
            port = int(port)
            servers.append(
                Proxy(
                    host=host, port=port,
                    user=user, password=password,
                    proxy_type=self.proxy_type,
                )
            )
        if servers:
            self._servers = servers
            self._servers_iter = cycle(self._servers)

    def random_server(self):
        return randomizer.choice(self._servers)

    def next_server(self):
        return next(self._servers_iter)

    def reload(self):
        if self._source['type'] == 'list':
            pass
        else:
            self.load_source(
                self._source['type'],
                self._source['location'],
            )

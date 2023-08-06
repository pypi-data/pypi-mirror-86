import collections
import contextlib
import functools
import json
import random
import re
import threading
from typing import Callable, Iterator
from urllib.parse import urljoin
import requests


def content_type(response, **patterns):
    """Return name for response's content-type based on regular expression matches."""
    ct = response.headers.get('content-type', '')
    matches = (name for name, pattern in patterns.items() if re.match(pattern, ct))
    return next(matches, '')


def validate(response):
    """Return validation headers from response translated for modification."""
    headers = response.headers
    validators = {'etag': 'if-match', 'last-modified': 'if-unmodified-since'}
    return {validators[key]: headers[key] for key in validators if key in headers}


class Client(requests.Session):
    """A Session which sends requests to a base url.

    Args:
        url: base url for requests
        trailing: trailing chars (e.g. /) appended to the url
        headers: additional headers to include in requests
        **attrs: additional Session attributes
    """

    def __init__(self, url, trailing='', headers=(), **attrs):
        super().__init__()
        self.__setstate__(attrs)
        self.headers.update(headers)
        self.trailing = trailing
        self.url = url.rstrip('/') + '/'

    @classmethod
    def clone(cls, other, path='', **kwargs):
        kwargs.update(other.__getstate__())
        return cls(urljoin(other.url, path), trailing=other.trailing, **kwargs)

    def __repr__(self):
        return f'{type(self).__name__}({self.url}... {self.trailing})'

    def __truediv__(self, path: str) -> 'Client':
        """Return a cloned client with appended path."""
        return type(self).clone(self, path)

    def request(self, method, path, **kwargs):
        """Send request with relative or absolute path and return response."""
        url = urljoin(self.url, path).rstrip('/') + self.trailing
        return super().request(method, url, **kwargs)

    def get(self, path='', **kwargs):
        """GET request with optional path."""
        return self.request('GET', path, **kwargs)

    def options(self, path='', **kwargs):
        """OPTIONS request with optional path."""
        return self.request('OPTIONS', path, **kwargs)

    def head(self, path='', allow_redirects=False, **kwargs):
        """HEAD request with optional path."""
        return self.request('HEAD', path, allow_redirects=allow_redirects, **kwargs)

    def post(self, path='', json=None, **kwargs):
        """POST request with optional path and json body."""
        return self.request('POST', path, json=json, **kwargs)

    def put(self, path='', json=None, **kwargs):
        """PUT request with optional path and json body."""
        return self.request('PUT', path, json=json, **kwargs)

    def patch(self, path='', json=None, **kwargs):
        """PATCH request with optional path and json body."""
        return self.request('PATCH', path, json=json, **kwargs)

    def delete(self, path='', **kwargs):
        """DELETE request with optional path."""
        return self.request('DELETE', path, **kwargs)


class Resource(Client):
    """A [Client][clients.base.Client] which returns json content and has syntactic support for requests."""

    client = property(Client.clone, doc="upcasted [Client][clients.base.Client]")
    __getitem__ = Client.get
    __setitem__ = Client.put
    __delitem__ = Client.delete
    __getattr__ = Client.__truediv__
    content_type = functools.partial(content_type, text='text/', json=r'application/(\w|\.)*\+?json')

    def request(self, method, path, **kwargs):
        """Send request with path and return processed content."""
        response = super().request(method, path, **kwargs)
        response.raise_for_status()
        if self.content_type(response) == 'json':
            return response.json()
        return response.text if response.encoding else response.content

    def iter(self, path: str = '', **kwargs) -> Iterator:
        """Iterate lines or chunks from streamed GET request."""
        response = super().request('GET', path, stream=True, **kwargs)
        response.raise_for_status()
        content_type = self.content_type(response)
        if content_type == 'json':
            response.encoding = response.encoding or 'utf8'
            return map(json.loads, response.iter_lines(decode_unicode=True))
        if response.encoding or content_type == 'text':
            return response.iter_lines(decode_unicode=response.encoding)
        return iter(response)

    __iter__ = iter

    def __contains__(self, path: str):
        """Return whether endpoint exists according to HEAD request."""
        return super().request('HEAD', path, allow_redirects=False).ok

    def __call__(self, path: str = '', **params):
        """GET request with params."""
        return self.get(path, params=params)

    def updater(self, path='', **kwargs):
        response = super().request('GET', path, **kwargs)
        response.raise_for_status()
        kwargs['headers'] = dict(kwargs.get('headers', {}), **validate(response))
        yield self.put(path, (yield response.json()), **kwargs)

    @contextlib.contextmanager
    def updating(self, path: str = '', **kwargs):
        """Provisional context manager to GET and conditionally PUT json data."""
        updater = self.updater(path, **kwargs)
        json = next(updater)
        yield json
        updater.send(json)

    def update(self, path: str = '', callback: Callable = None, **json):
        """PATCH request with json params.

        Args:
            callback: optionally update with GET and validated PUT.
                ``callback`` is called on the json result with keyword params, i.e.,
                ``dict`` correctly implements the simple update case.
        """
        if callback is None:
            return self.patch(path, json=json)
        updater = self.updater(path)
        return updater.send(callback(next(updater), **json))

    def create(self, path: str = '', json=None, **kwargs) -> str:
        """POST request and return location."""
        response = super().request('POST', path, json=json, **kwargs)
        response.raise_for_status()
        return response.headers.get('location')

    def download(self, file, path: str = '', **kwargs):
        """Output streamed GET request to file."""
        response = super().request('GET', path, stream=True, **kwargs)
        response.raise_for_status()
        for chunk in response:
            file.write(chunk)
        return file

    def authorize(self, path: str = '', **kwargs) -> dict:
        """Acquire oauth access token and set ``Authorization`` header."""
        method = 'GET' if {'json', 'data'}.isdisjoint(kwargs) else 'POST'
        result = self.request(method, path, **kwargs)
        self.headers['authorization'] = f"{result['token_type']} {result['access_token']}"
        return result


class Remote(Client):
    """A [Client][clients.base.Client] which defaults to posts with json bodies, i.e., RPC.

    Args:
        url: base url for requests
        json: default json body for all calls
        **kwargs: same options as [Client][clients.base.Client]
    """

    client = Resource.client
    __getattr__ = Resource.__getattr__

    def __init__(self, url: str, json=(), **kwargs):
        super().__init__(url, **kwargs)
        self.json = dict(json)

    @classmethod
    def clone(cls, other, path=''):
        return Client.clone.__func__(cls, other, path, json=other.json)

    def __call__(self, path: str = '', **json):
        """POST request with json body and [check][clients.base.Remote.check] result."""
        response = self.post(path, json=dict(self.json, **json))
        response.raise_for_status()
        return self.check(response.json())

    @staticmethod
    def check(result):
        """Override to return result or raise error, for APIs which don't use status codes."""
        return result


class Graph(Remote):
    """A [Remote][clients.base.Remote] client which executes GraphQL queries."""

    Error = requests.HTTPError

    @classmethod
    def check(cls, result: dict):
        """Return ``data`` or raise ``errors``."""
        for error in result.get('errors', ()):
            raise cls.Error(error)
        return result.get('data')

    def execute(self, query: str, **variables):
        """Execute query over POST."""
        return self(query=query, variables=variables)


class Stats(collections.Counter):
    """Thread-safe Counter.

    Context manager tracks number of active connections and errors.
    """

    def __init__(self):
        self.lock = threading.Lock()

    def add(self, **kwargs):
        """Atomically add data."""
        with self.lock:
            self.update(kwargs)

    def __enter__(self):
        self.add(connections=1)
        return self

    def __exit__(self, *args):
        self.add(connections=-1, errors=int(any(args)))


class Proxy(Client):
    """An extensible embedded proxy client to multiple hosts.

    The default implementation provides load balancing based on active connections.
    It does not provide error handling or retrying.

    Args:
        *urls: base urls for requests
        **kwargs: same options as [Client][clients.base.Client]
    """

    Stats = Stats

    def __init__(self, *urls: str, **kwargs):
        super().__init__('', **kwargs)
        self.urls = {(url.rstrip('/') + '/'): self.Stats() for url in urls}

    @classmethod
    def clone(cls, other, path=''):
        urls = (urljoin(url, path) for url in other.urls)
        return cls(*urls, trailing=other.trailing, **other.__getstate__())

    def priority(self, url: str):
        """Return comparable priority for url.

        Minimizes errors, failures (500s), and active connections.
        None may be used to eliminate from consideration.
        """
        stats = self.urls[url]
        return tuple(stats[key] for key in ('errors', 'failures', 'connections'))

    def choice(self, method: str) -> str:
        """Return chosen url according to priority.

        Args:
            method: placeholder for extensions which distinguish read/write requests
        """
        priorities = collections.defaultdict(list)  # type: dict
        for url in self.urls:
            priorities[self.priority(url)].append(url)
        priorities.pop(None, None)
        return random.choice(priorities[min(priorities)])

    def request(self, method, path, **kwargs):
        """Send request with relative or absolute path and return response."""
        url = self.choice(method)
        with self.urls[url] as stats:
            response = super().request(method, urljoin(url, path), **kwargs)
        stats.add(failures=int(response.status_code >= 500))
        return response

from __future__ import unicode_literals

import logging

from collections import OrderedDict
from functools import wraps


logger = logging.getLogger(__name__)


class LruCache(OrderedDict):
    def __init__(self, max_size=1024, default_value=''):
        if max_size <= 0:
            raise ValueError('Invalid size')
        OrderedDict.__init__(self)
        self._max_size = max_size
        self._check_limit()
        self._default_value = default_value

    def get_max_size(self):
        return self._max_size

    def hit(self, key):
        if key in self:
            val = self[key]
            self[key] = val
            # logger.debug('HIT: %r -> %r', key, val)
            return val
        # logger.debug('MISS: %r', key)
        return None

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self, key, self._default_value if value is None else value)
        self._check_limit()

    def _check_limit(self):
        while len(self) > self._max_size:
            # delete oldest entries
            k = list(self)[0]
            del self[k]


class SearchCache(LruCache):
    def __init__(self, func):
        super(SearchCache, self).__init__()
        self._func = func

    def __call__(self, *args, **kwargs):
        key = SearchKey(**kwargs)
        cached_result = self.hit(key)
        logger.info("Search cache miss" if cached_result is None
                    else "Search cache hit")
        if cached_result is None:
            cached_result = self._func(*args, **kwargs)
            self[key] = cached_result

        return cached_result


class SearchKey(object):
    def __init__(self, **kwargs):
        fixed_query = self.fix_query(kwargs["query"])
        self._query = tuple(sorted(fixed_query.items()))
        self._exact = kwargs["exact"]
        self._hash = None

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self._exact)
            self._hash ^= hash(repr(self._query))

        return self._hash

    def __eq__(self, other):
        if not isinstance(other, SearchKey):
            return False

        return self._exact == other._exact and \
            self._query == other._query

    @staticmethod
    def fix_query(query):
        """
        Removes some query parameters that otherwise will lead to a cache miss.
        Eg: 'track_no' since we can't query TIDAL for a specific album's track.
        :param query: query dictionary
        :return: sanitized query dictionary
        """
        query.pop("track_no", None)
        return query


track_cache = LruCache(max_size=1024*16)
image_cache = LruCache(max_size=1024*16)


def cache_track(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        item = func(*args, **kwargs)
        track_cache[item.uri] = item
        return item
    return wrapper


def cache_image(func):
    @wraps(func)
    def wrapper(tidal_item, *args, **kwargs):
        item = func(tidal_item, *args, **kwargs)
        image_cache[item.uri] = tidal_item.image
        return item
    return wrapper


def with_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        uri = args[-1]
        track = track_cache.hit(uri)
        if track is not None:
            logger.debug("Found cached: %s", uri)
            return [track]
        return func(*args, **kwargs)
    return wrapper

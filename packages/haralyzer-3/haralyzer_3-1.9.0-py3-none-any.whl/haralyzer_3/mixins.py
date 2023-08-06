"""Mixin Objects that allow for shared methods"""
from cached_property import cached_property
from six.moves.collections_abc import MutableMapping


def iteritems(dic: dict):
    """
    Shared function that returns and iter of dic items
    :param dic: Dict to iterate
    :return: Iterator of dict items
    """
    return iter(dic.items())


class MimicDict(MutableMapping):
    # pylint: disable=invalid-name
    """Mixin for functions to mimic a dictionary for backward compatibility"""

    def __getitem__(self, item):
        return self.raw_entry[item]

    def __len__(self):
        return len(self.raw_entry)

    def __delitem__(self, key):
        del self.raw_entry[key]

    def __iter__(self):
        return iter(self.raw_entry)

    def __setitem__(self, key, value):
        self.raw_entry[key] = value


class HttpTransaction(MimicDict):
    """Class that is used to make a Request or Response object as a dict with headers"""

    # pylint: disable=invalid-name
    def __init__(self, entry):
        super().__init__()
        self.raw_entry = entry

    # Base class gets properties that belong to both request/response
    @cached_property
    def headers(self) -> dict:
        """Returns a dict of headers"""
        return {x["name"].lower(): x["value"] for x in self.raw_entry["headers"]}

    @cached_property
    def bodySize(self) -> int:
        """:returns request bodySize"""
        return int(self.raw_entry["bodySize"])

    @cached_property
    def cookies(self) -> dict:
        """:returns list of cookies"""
        return self.raw_entry["cookies"]

    @cached_property
    def headersSize(self):
        """:returns request headerSize"""
        return int(self.raw_entry["headersSize"])

    @cached_property
    def httpVersion(self) -> str:
        """:returns HTTP version """
        return self.raw_entry["httpVersion"]

    @cached_property
    def cacheControl(self):
        """:returns cache-control"""
        return self.headers.get("cache-control")

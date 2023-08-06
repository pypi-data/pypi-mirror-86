"""Handles request cards caching."""
from pathlib import Path
from typing import List, Optional, Set

from appdirs import user_cache_dir
from diskcache import Index
from pydantic.main import BaseModel

from . import __app_name__, __version__
from .cards import Card
from .query import QueryType


class CacheManager(BaseModel):
    """Manages card cache."""

    path: Path
    _index: Index

    _SETS_KEY: str = "sets"

    class Config:  # pylint: disable=missing-class-docstring
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True

    def __init__(self, path: Optional[Path] = None) -> None:
        path = path or CacheManager.default_path()

        super().__init__(path=path)

        self._index = self._create_index()

    @staticmethod
    def default_path() -> Path:
        """Return a default cache directory"""
        return Path(user_cache_dir(__app_name__, version=__version__))

    def _create_index(self) -> Index:
        """Create a disk index."""
        index = Index(str(self.path))
        if self._SETS_KEY not in index:
            index[self._SETS_KEY] = {}
        return index

    def has_cache(self, query: QueryType, sets: List[str]) -> bool:
        """Return ``True`` if ``index`` has a card cache."""
        try:
            self._index[query]
        except KeyError:
            return False

        if set(sets).issubset(self._cached_sets(query)):
            return True

        return False

    def write_cache(self, query: QueryType, sets: List[str], cards: List[Card]):
        """Write cards to the local cache."""
        self._index[query] = cards
        self._set_cached_sets(query, sets)

    def read_cache(self, query: QueryType) -> List[Card]:
        """Read cards from the local cache."""
        return self._index.get(query, [])

    def clear(self):
        """Clear the cache."""
        self._index.clear()

    def _cached_sets(self, query: QueryType) -> Set[str]:
        return self._index.get(self._SETS_KEY, {}).get(query, set())

    def _set_cached_sets(self, query: QueryType, sets: List[str]):
        cached_sets = self._index.get(self._SETS_KEY, {})
        cached_sets[query] = cached_sets.get(query, set()).union(sets)
        self._index[self._SETS_KEY] = cached_sets

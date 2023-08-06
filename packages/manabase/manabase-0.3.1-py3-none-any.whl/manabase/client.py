"""Fetch data from [scryfall](https://scryfall.com/)."""
import time
from typing import Dict, List, Optional

import requests
from pydantic import ValidationError

from .cache import CacheManager
from .cards import Card
from .query import SetQueryBuilder


class Client:
    """A client for the scryfall API."""

    API_URL = "https://api.scryfall.com"

    def __init__(self, api_url: str = API_URL, cache: Optional[CacheManager] = None):
        self.api_url = api_url
        self.cache = cache

    def route(self, path: str) -> str:
        """Build an URL endpoint from a relative path.

        Example::

        ```python
        >>> from manabase.client import Client
        >>> client = Client()
        >>> client.route("cards/search")
        'https://api.scryfall.com/cards/search'
        """
        return "/".join([self.api_url, path])

    def fetch(self, builder: SetQueryBuilder) -> List[Card]:
        """Fetch a filtered list of cards."""
        if self.cache and self.cache.has_cache(builder.type, builder.sets):
            return self.cache.read_cache(builder.type)

        query = builder.build()

        cards = self._fetch_cards(query)

        if self.cache is not None:
            self.cache.write_cache(builder.type, builder.sets, cards)

        return cards

    def _fetch_cards(self, query: str) -> List[Card]:
        data = self._fetch_all_pages(query)
        cards = []

        for obj in data:

            if "produced_mana" not in obj:
                # Fetch lands don't have the ``produced_mana`` field.
                obj.update({"produced_mana": []})

            try:
                model = Card(**obj)
            except ValidationError:
                continue

            cards.append(model)

        return cards

    def _fetch_all_pages(self, query: str, page: int = 1) -> List[Dict]:
        """Fetch all pages, draining paginated content."""
        params = {"q": query, "page": page}
        response = requests.get(self.route("cards/search"), params=params)

        data = response.json()

        objects: List[Dict] = data["data"]

        if data["has_more"]:
            # Go easy on scryfall servers.
            time.sleep(0.1)

            next_objects: List[Dict] = self._fetch_all_pages(query, page + 1)
            objects.extend(next_objects)

        return objects

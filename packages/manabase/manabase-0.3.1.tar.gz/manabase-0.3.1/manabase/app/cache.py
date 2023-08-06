"""Cache management."""
import typer

from ..cache import CacheManager


def clear_cache(ctx: typer.Context):
    """Clear the cache."""
    cache: CacheManager = ctx.obj.cache
    cache.clear()

    typer.echo("Cache cleared.")

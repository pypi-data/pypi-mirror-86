"""Presets management."""
from typing import Optional

import typer

from ..settings import GenerationPreset, UserSettings

app = typer.Typer()


@app.callback()
def main():
    """Manage generation presets."""


@app.command()
def new(  # pylint: disable=too-many-arguments, too-many-locals
    ctx: typer.Context,
    name: str,
    filters: Optional[str] = None,
    lands: Optional[int] = None,
    occurrences: Optional[int] = None,
    priorities: Optional[str] = None,
    filler_weights: Optional[str] = None,
    rocks: Optional[int] = None,
    rock_filters: Optional[str] = None,
    rock_priorities: Optional[str] = None,
    sets: Optional[str] = None,
):
    """Create a new preset."""
    settings: UserSettings = ctx.obj.settings

    if name in settings.presets:
        typer.echo(typer.style(f'Preset "{name}" already exists.', fg=typer.colors.RED))
        return

    preset = GenerationPreset(
        name=name,
        filters=filters,
        lands=lands,
        occurrences=occurrences,
        priorities=priorities,
        filler_weights=filler_weights,
        rocks=rocks,
        rock_filters=rock_filters,
        rock_priorities=rock_priorities,
        sets=sets,
    )
    settings.presets[name] = preset
    settings.active = name

    settings.save()

    typer.echo(f'Created preset "{name}".')


@app.command()
def use(ctx: typer.Context, name: str):
    """Set the active preset."""
    settings: UserSettings = ctx.obj.settings

    if name not in settings.presets:
        typer.echo(typer.style(f'No preset named "{name}".', fg=typer.colors.RED))
        return

    if settings.active == name:
        typer.echo(f'"{name}" is already the active preset.')
        return

    settings.active = name
    settings.save()

    typer.echo(f'Active preset is now "{name}".')


@app.command()
def active(ctx: typer.Context):
    """Print the active preset."""
    settings: UserSettings = ctx.obj.settings

    if not settings.active:
        typer.echo("There is no active preset.")
    else:
        typer.echo(settings.active)


@app.command(name="list")
def list_(ctx: typer.Context):
    """List all user presets."""
    settings: UserSettings = ctx.obj.settings

    if not settings.presets:
        msg = "No preset saved. Create one with `manabase presets new`."
    else:
        msg = "\n".join([f"- {preset}" for preset in settings.presets])

    typer.echo(msg)


@app.command()
def show(ctx: typer.Context, name: str):
    """Show a user preset options."""
    settings: UserSettings = ctx.obj.settings

    if name not in settings.presets:
        typer.echo(typer.style(f'No preset named "{name}".', fg=typer.colors.RED))
        return

    preset = settings.presets[name]

    msg = preset.name

    for key, value in preset.dict().items():

        if key == "name" or value is None:
            continue

        msg += f"\n- {key}: {value}"

    typer.echo(msg)


@app.command()
def update(  # pylint: disable=too-many-arguments, too-many-locals
    ctx: typer.Context,
    name: str,
    filters: Optional[str] = None,
    lands: Optional[int] = None,
    occurrences: Optional[int] = None,
    priorities: Optional[str] = None,
    filler_weights: Optional[str] = None,
    rocks: Optional[int] = None,
    rock_filters: Optional[str] = None,
    rock_priorities: Optional[str] = None,
    sets: Optional[str] = None,
):
    """Update a user preset.

    It will replace all options with the one you define.
    """
    settings: UserSettings = ctx.obj.settings

    if name not in settings.presets:
        typer.echo(typer.style(f'No preset named "{name}".', fg=typer.colors.RED))
        return

    preset = settings.presets[name]

    preset.name = name
    preset.filters = filters
    preset.lands = lands
    preset.occurrences = occurrences
    preset.priorities = priorities
    preset.filler_weights = filler_weights
    preset.rocks = rocks
    preset.rock_filters = rock_filters
    preset.rock_priorities = rock_priorities
    preset.sets = sets

    settings.save()

    typer.echo(f'Updated preset "{name}".')


@app.command()
def patch(  # pylint: disable=too-many-arguments, too-many-locals
    ctx: typer.Context,
    name: str,
    filters: Optional[str] = None,
    lands: Optional[int] = None,
    occurrences: Optional[int] = None,
    priorities: Optional[str] = None,
    filler_weights: Optional[str] = None,
    rocks: Optional[int] = None,
    rock_filters: Optional[str] = None,
    rock_priorities: Optional[str] = None,
    sets: Optional[str] = None,
):
    """Patch a user preset.

    It will add options you define to an existing preset.
    """
    settings: UserSettings = ctx.obj.settings

    if name not in settings.presets:
        typer.echo(typer.style(f'No preset named "{name}".', fg=typer.colors.RED))
        return

    preset = settings.presets[name]

    if filters is not None:
        preset.filters = filters
    if lands is not None:
        preset.lands = lands
    if occurrences is not None:
        preset.occurrences = occurrences
    if priorities is not None:
        preset.priorities = priorities
    if filler_weights is not None:
        preset.filler_weights = filler_weights
    if rocks is not None:
        preset.rocks = rocks
    if rock_filters is not None:
        preset.rock_filters = rock_filters
    if rock_priorities is not None:
        preset.rock_priorities = rock_priorities
    if sets is not None:
        preset.sets = sets

    settings.presets[name] = preset

    settings.save()

    typer.echo(f'Patched preset "{name}".')


@app.command()
def delete(ctx: typer.Context, name: str):
    """Delete a user preset."""
    settings: UserSettings = ctx.obj.settings

    if name not in settings.presets:
        typer.echo(typer.style(f'No preset named "{name}".', fg=typer.colors.RED))
        return

    del settings.presets[name]

    settings.save()

    typer.echo(f'Deleted preset "{name}".')

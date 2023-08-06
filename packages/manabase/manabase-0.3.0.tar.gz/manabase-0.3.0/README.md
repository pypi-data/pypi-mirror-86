# manabase

Landing rock solid mana bases for your decks.

Manabase is a command-line tool that helps you generate a mana base for your
Magic: The Gathering decks.

It uses [scryfall](https://scryfall.com/) as its source of truth.

## Installation

Manabase is available on [PyPI](https://pypi.org/project/manabase/)
Install manabase using `pip`:

```bash
pip install --user manabase
```

## Usage

Manabase offers a primary command, `manabase`, that generates a list of lands
for a set of colors.

### Filters

Manabase includes a set of powerful filters, defining which type of lands are
allowed in the output list.

These type of lands are called land cycles, and are defined by
[MTG Gamepedia](https://mtg.gamepedia.com/Dual_land).

Following is a list of supported cycles, and the name of the corresponding
filter:

- [`battle`](https://mtg.gamepedia.com/Battle_land): Battle for Zendikar dual lands.
- [`bond`](https://mtg.gamepedia.com/Bond_land): Battlebond and Commander Legends crowd lands.
- [`bounce`](https://mtg.gamepedia.com/Bounce_land): Ravnica bounce lands.
- [`check`](https://mtg.gamepedia.com/Check_land): Ixalan and Innistrad check lands.
- [`cycling`](https://mtg.gamepedia.com/Cycling_land#Dual-colored_Cycling_Lands):
  Amonkhet cycling lands.
- [`fast`](https://mtg.gamepedia.com/Fast_land): Mirrodin and Kaladesh fast lands.
- [`fetch`](https://mtg.gamepedia.com/Fetch_land): Onslaught and Zendikar fetch lands.
- [`filter`](https://mtg.gamepedia.com/Filter_land): Odyssey and Future Sight filter lands.
- [`horizon`](https://mtg.gamepedia.com/Horizon_land): Future Sight and Modern Horizons horizon lands.
- [`original`](https://mtg.gamepedia.com/Dual_land#Original_dual_lands):
  The original dual lands.
- [`pain`](https://mtg.gamepedia.com/Pain_land): Ice Age and Apocalypse pain lands.
- [`reveal`](https://mtg.gamepedia.com/Reveal_land): Innistrad reveal lands.
- [`scry`](https://mtg.gamepedia.com/Scry_land): Theros and M21 scry lands.
- [`shock`](https://mtg.gamepedia.com/Shock_land): Ravnica shock lands.

Additionally, two color-related filters are provided:

These are:

- `producer`: This filter checks if the land produces mana of the given colors.
- `reference`: This filter checks if a reference to a land type of the given
  colors is contained in the card text.

Without these filters, all colors could be matched.

Examples:

`fetch` will accept all fetch lands.
`producer` will accept all lands that can produce your colors.

### Operators

Filters can be combined using four operators:

- `&`: Accepts only cards matching both filters.
- `|`: Accepts cards matching either filter.
- `^`: Accepts cards matching one filter or the other, but not both.
- `~`: Inverts the following filter results.

Moreover, you can group operators and filters using parenthesis to
control operator precedence.

Examples:

- `reference & fetch` would match only fetch lands respecting your colors.
- `(producer & original) | (reference & fetch)` would match either original
  lands producing your colors, or fetch lands of your colors.

### Filter arguments

Finally, some filters can take arguments to control their behavior.

`producer` and `reference` each take `exclusive` and `minimum_count` arguments.

`exclusive`, which is true by default, prevents cards matching colors other than
yours. For example, if you asked for white and blue, a white and red land would
be excluded, because it contains red.

`minimum_count` sets the number of colors a land should match, among your colors,
before being accepted. By default this is 2, which means lands have to produce
or reference at least two of your colors to be accepted.

This filters can help you define a better behavior, for example for fetch lands
it makes sense to disable the `exclusive` argument and set the `minimum_count`
to 1, so that all fetch lands matching at least one of your colors are included.

To override arguments, specify your argument values in the right order, between
curly braces, separated by commas.

Examples:

- `producer { 0, 3 }` would match all lands producing at least three of your
  colors, without excluding other colors.
- `reference { 0, 1 } & fetch` would match fetch lands producing at least one
  of your colors, without excluding other colors.

### Commands

In the following examples, we are using the `manabase` command to generate
a set of lands for a white, blue and black deck.

Generate a set of lands using default settings:

```bash
manabase WUB
```

Generate a set of 37 maximum lands, with 1 occurrence of each land:

```bash
manabase --lands=37 --occurrences WUB
```

Generate a list of only fetch lands and original dual lands.

```bash
manabase --filters="(producer & original) | (reference & fetch)" WUB
```

### Presets

Specifying command-line arguments can be a bit cumbersome, especially for the
`--filters` option.

A generation preset allows you to specify any **options** the `generate` command
takes in, and apply them automatically.

For the following sections, it is assumed the preset name is `default`.

#### Creating a preset

To create a new preset, use the `manabase presets new` command, with a name for
the new preset and any option the `generate` command can take.

```bash
manabase presets new default --filters="(producer & (original | shock)) | (reference & fetch)" --lands=37 --occurrences=1
```

#### Selecting the active preset

The active preset is the one used automatically when using the
`generate` command.

You can activate an existing preset with the following command.

```bash
manabase presets use default
```

Note: when you create a new preset, it is automatically activated
for you.

#### Printing the active preset

You can print the active preset with the following command.

```bash
manabase presets active
```

#### Listing existing presets

You can list existing preset names with the following command.

```bash
manabase presets list
```

#### Printing a preset

To print a preset content to the terminal, use the following command.

```bash
manabase presets show default
```

#### Updating a preset

Updating a preset replaces all its options with new ones.

If you meant to add a new option, or update a single option, use the `patch` subcommand.

```bash
manabase presets update default --lands=35
```

#### Patching a preset

Patching a preset adds a new option or updates an existing one.

```bash
manabase presets patch default --occurrences=4
```

#### Deleting a preset

Deleting a presets erases its file from disk.

```bash
manabase presets delete default
```

## Contributing

This package uses [`poetry`](https://python-poetry.org/) to manage its
dependencies.

### Installing

[Install poetry](https://python-poetry.org/docs/#installation).

Clone this repository:

```bash
git clone https://github.com/Aphosis/manabase
cd manabase
```

Install manabase for development:

```bash
poetry install
```

### Tests

Tests are written using [pytest](https://docs.pytest.org/en/stable/).

Once `manabase` has been installed, you can run tests to check if your
changes did not introduce regressions.

To run the test suite, `cd` into the `manabase` folder, then run:

```bash
pytest
```

Pytest is configured in `pyproject.toml`, you do not need to specify any
extra arguments.

## License

This tool is licensed under MIT.

## Non affiliation disclaimer

Manabase is not affiliated, associated, authorized, endorsed by, or in any way
officially connected with Wizards of the Coast, or any of its subsidiaries or
its affiliates.

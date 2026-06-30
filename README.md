# Spoons API

A CLI tool that calculates the cheapest way to get drunk at a given Wetherspoons venue, by ranking every alcoholic drink on the menu by cost per unit of alcohol.

It works by talking to the same internal API the Wetherspoons app uses, pulling the full menu for a chosen venue, then parsing prices, ABV, and serving sizes out of the (often inconsistent) menu data to compute a true cost-per-unit ranking.

## Usage

```bash
uv run main.py
```

You'll be prompted to search for and select a venue, then the tool will fetch its menus and print every drink found, sorted from cheapest to most expensive per unit of alcohol.

## Development

Install dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest
```

Tests fetch real data via the repositories, deserialise into models, re-serialise back to dicts, and check nothing was lost or mangled along the way.

## TODO

- Calculate units of alcohol in each pitcher
- Calculate units of alcohol in each double shot
- Figure out how guest ales are represented (units/ABV aren't always available)
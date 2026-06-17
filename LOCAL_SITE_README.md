# Local Documentation Site

Instructions for building and running the documentation website locally.

## Prerequisites

This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/) for dependency management.

## Install dependencies

```bash
uv sync --only-group doc
```

## Run the site locally

```bash
uv run mkdocs serve
```

The site will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Build the static site

```bash
uv run mkdocs build
```

Output is written to `site/`.

## References

- [MkDocs Documentation](https://www.mkdocs.org/)
- [MkDocs Material Theme](https://squidfunk.github.io/mkdocs-material/)

## Quick run

```bash
uv sync --only-group doc
uv run mkdocs serve
```

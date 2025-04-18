# mirror-docs

## Description

This project automates the process of mirroring raw HTML documentation from a given framework, converting it to Markdown, and generating a sitemap for indexing local full-docs references.

## Usage

1.  Use `00-mirror.sh` to mirror the HTML documentation from a website:

    ```bash
    ./00-mirror.sh <domain>
    ```

2.  Use `01-md.py` to convert the HTML files to Markdown:

    ```bash
    python 01-md.py
    ```

3.  Use `02-sitemap.sh` to generate a sitemap:

    ```bash
    ./02-sitemap.sh
    ```

## Memory Bank

The `memory-bank/` directory contains documentation about the project's design, implementation, and progress.

## License

[MIT](LICENSE)

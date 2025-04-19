# mirror-docs

## Description

This project automates the process of mirroring raw HTML documentation from a given framework, converting it to Markdown, and generating a sitemap for indexing local full-docs references.

## Usage

To use the `mirror-docs` CLI tool:

```bash
python mirror_docs.py --domain <domain> --docs-path <docs_path> --output-dir <output_dir> --sitemap-file <sitemap_file>
```

*   `<domain>`: The base domain URL (e.g., `https://www.example.com`).
*   `<docs_path>`: The specific path on the domain containing the documentation (e.g., `/docs`).
*   `<output_dir>`: The local directory where the mirrored HTML and generated Markdown will be stored (e.g., `./output`).
*   `<sitemap_file>`: The name of the output sitemap file (e.g., `sitemap.txt`).

Example:

```bash
uv run mirror_docs.py --domain https://www.instantdb.com --docs-path /docs --output-dir ./instantdb_docs --sitemap-file sitemap.txt
```

## Memory Bank

The `memory-bank/` directory contains documentation about the project's design, implementation, and progress.

## License

[MIT](LICENSE)

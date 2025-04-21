# Progress: mirror-docs

## What Works

*   The core `mirror_docs.py` CLI script is functional:
    *   Accepts a URL as input.
    *   Mirrors HTML documentation using `wget` (with User-Agent and improved error handling), limiting scope with `--include-directories`.
    *   Extracts main content using `readability-lxml`.
    *   Converts extracted HTML to Markdown using `markdownify`.
    *   Extracts HTML `<title>` tags using `BeautifulSoup`.
    *   Generates a `sitemap.txt` file containing relative Markdown paths and corresponding page titles (`path :: title`), merging with existing entries.
    *   Stores mirrored HTML and generated Markdown in the specified output directory structure.
*   The `README.md` file provides comprehensive usage instructions, explains the benefits (especially for AI integration), and includes an example `.clinerule`.
*   The memory bank structure is established and being updated.
*   Project dependencies are managed via `pyproject.toml` and `uv`.
*   Classifiers have been added to `pyproject.toml`.
*   Distribution packages have been generated.
*   Configured `pyproject.toml` for PyPI publishing.
*   Created GitHub Actions workflow for automated PyPI publishing.

## What's Left to Build

*   Testing the script with a wider variety of documentation sites to ensure robustness.
*   Considering future enhancements: dependency checks (`wget`), configuration files, incremental updates, modular site organization.

## Current Status

The core functionality of mirroring documentation, converting it to Markdown, and generating a title-enhanced sitemap is implemented. The project is positioned as a tool to create local documentation knowledge bases for improved developer workflow and AI assistant integration. Documentation (`README.md`) reflects this. Focus is shifting towards testing, refinement, and considering future enhancements.

## Known Issues

*   Robustness across diverse website structures and potential edge cases in HTML parsing/conversion needs further testing.
*   `wget` dependency is assumed; no explicit check is performed.

## Evolution of Project Decisions

*   The project's focus shifted from simple mirroring/conversion to emphasizing the creation of local, token-efficient knowledge bases for AI integration. This led to the enhancement of the sitemap with page titles and detailed `README.md` updates including the `.clinerule` concept.
*   The decision to use Markdown as the primary format was based on its simplicity and wide support.
*   The decision to use Python for scripting was based on its rich ecosystem of libraries.
*   The decision to use shell scripts for automation was based on their simplicity and ease of use.

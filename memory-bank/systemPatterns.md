# System Patterns: mirror-docs

## System Architecture

The system will be implemented as a single Python CLI script (`mirror_docs.py`) that encapsulates all functionality.

## Key Technical Decisions

*   **Python for CLI and processing:** Python is used for the CLI interface, data acquisition, transformation, and sitemap generation.
*   **Markdown as the primary format:** Markdown remains the chosen format for its simplicity and wide support.
*   **argparse for CLI argument parsing:** The `argparse` library will be used to handle command-line arguments.

## Design Patterns

*   **Command Pattern:** The CLI script acts as a command, taking arguments and executing the mirroring, conversion, and sitemap generation process.

## Component Relationships

The script will internally manage the flow of data from mirroring to conversion to sitemap generation.

## Critical Implementation Paths

*   The `mirror_docs.py` script will handle all steps: mirroring, conversion, and sitemap generation.
*   The script will take command-line arguments for domain, documentation path, output directory, and sitemap file name.
*   The script will use libraries like `requests` or `wget` (via `subprocess`) for mirroring, `readability-lxml` for content extraction, and `markdownify` for HTML to Markdown conversion.

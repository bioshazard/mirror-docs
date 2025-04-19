# Technical Context: mirror-docs

## Technologies Used

*   **Python:** Used for the CLI tool, data acquisition, transformation, and sitemap generation.
*   **Markdown:** Used as the primary format for storing and presenting documentation.
*   **argparse:** Used for parsing command-line arguments.
*   **requests (or wget via subprocess):** Used for mirroring HTML documentation.
*   **readability-lxml:** Used for extracting the main content from HTML.
*   **markdownify:** Used for converting HTML to Markdown.
*   **pyproject.toml:** Used for managing Python project dependencies and build configuration.
*   **uv.lock:** Used for managing Python project dependencies.

## Development Setup

*   **Python Environment:** Requires a Python environment with the necessary dependencies installed (see `pyproject.toml`).

## Technical Constraints

*   **Dependency Management:** Managing dependencies for Python scripts.
*   **Data Source Variability:** Different documentation sources may require different acquisition and transformation strategies.

## Dependencies

*   Dependencies are managed using `pyproject.toml` and `uv.lock`.

## Tool Usage Patterns

*   **Text Editors:** Used for editing the Python script and documentation.
*   **Command-Line Interface (CLI):** Used for running the `mirror_docs.py` script.

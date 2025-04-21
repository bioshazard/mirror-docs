# mirror-docs 🪞📚

## Description

`mirror-docs` is a Python CLI tool that helps you create an offline, token-efficient, local knowledge base of the documentation for frameworks and libraries used in your project.

It mirrors HTML documentation 🪞 from a specified web source, converts the relevant content to Markdown ✍️, and generates a structured sitemap 🗺️.

This speeds up development and improves the accuracy of AI coding assistants (like Cline) by providing them with targeted, relevant context directly from the official docs, reducing the need for external API calls and saving context window tokens.

## Key Benefits ✨

*   **Reduced API/MCP Calls:** Saves costs and avoids potential rate limits associated with external documentation lookups by AI assistants or developers.
*   **Token Efficiency:** Markdown is significantly more compact than HTML, saving valuable context window space when feeding documentation to Large Language Models (LLMs).
*   **Speed & Offline Access:** Provides instant local access to documentation, independent of internet connectivity.
*   **Contextual Relevance:** Enables feeding specific, verified documentation sections to AI tools, leading to better, more accurate code generation and analysis.
*   **Version Alignment:** Ensures the local documentation can match the specific version of the library/framework used in your project by mirroring from the corresponding documentation URL.

## Usage 🚀

Run the `mirror_docs.py` script using `uv` (or your preferred Python environment manager):

```bash
uv run mirror_docs.py <url> [--output-dir <output_directory>]
```

**Arguments:**

*   `url`: (Required) The full URL to the documentation path you want to mirror (e.g., `https://react.dev/reference/rsc`).
*   `--output-dir`: (Optional) The local directory where mirrored content will be stored. Defaults to `.mirror-docs`. **It's recommended to add this directory to your project's `.gitignore` file.**

**Example (Mirroring React Reference Docs):**

```bash
# Run the tool (using default output directory '.mirror-docs')
uv run mirror_docs.py https://react.dev/reference

# Run the tool with a custom output directory
uv run mirror_docs.py https://react.dev/reference --output-dir my-react-docs
```

This will:
1.  Mirror HTML content from `https://react.dev/reference` into `<output_dir>/html/react.dev/reference/`.
2.  Convert the main content of each HTML page into Markdown files within `<output_dir>/markdown/react.dev/reference/`.
3.  Generate a sitemap at `<output_dir>/sitemap.txt` listing the Markdown files (relative to the `markdown` directory) and their titles like: `react.dev/reference/rsc/use-client.md :: 'use client' directive – React`

## Integrating with AI Assistants (like Cline) 🤖

The generated Markdown files and the `sitemap.txt` are powerful tools for providing context to AI assistants.

**How it Works:**

1.  **Sitemap:** The `sitemap.txt` provides a quick overview of the available documentation topics (via page titles) and their file paths.
2.  **Markdown Files:** These contain the core documentation content in a token-efficient format.

**Using a `.clinerule`:**

You can instruct an AI assistant like Cline to leverage these local docs by creating a `.clinerules/local_docs.md` file in your project's root directory with content similar to this:

```markdown
# Rule: Prioritize Local Mirrored Documentation

## Context

This project utilizes `mirror-docs` to maintain local copies of relevant framework/library documentation in the directory specified by `--output-dir` (defaulting to `.mirror-docs/`). This directory contains:

*   `markdown/`: Directory holding subdirectories for each mirrored domain (e.g., `markdown/react.dev/`). These contain the documentation converted to Markdown, preserving the original path structure.
*   `html/`: Directory holding the original mirrored HTML files, structured similarly to `markdown/`.
*   `sitemap.txt`: A file listing `domain/path/to/markdown.md :: Page Title`, relative to the `markdown/` directory.

## Instruction

When I ask questions or request code related to a framework/library for which local documentation exists in the mirrored docs directory (`.mirror-docs/` or the custom `--output-dir`):

1.  **Consult the Sitemap:** First, check the `sitemap.txt` in the root of the mirrored docs directory (e.g., `.mirror-docs/sitemap.txt`) to identify potentially relevant documentation pages based on their titles and paths (which include the domain).
2.  **Read Local Markdown:** If relevant pages are found, prioritize reading the corresponding Markdown file(s) from the `markdown/` directory. Use the `read_file` tool with the path constructed by joining the output directory base and `markdown/` followed by the relative path from the sitemap (e.g., `.mirror-docs/markdown/react.dev/reference/rsc/use-client.md`).
3.  **Synthesize Answer:** Base your answer or code generation primarily on the information found in the local Markdown files.
4.  **Fallback:** If the necessary information isn't found locally, you may then resort to general knowledge or external searches, but state that the local docs were consulted first.

**Example Scenario:** If I ask "How do I use the `useState` hook in React?", and the docs were mirrored to the default `.mirror-docs/`, you should:
    *   Look at `.mirror-docs/sitemap.txt`.
    *   Find a line like `react.dev/reference/react/useState.md :: useState – React`.
    *   Read the file `.mirror-docs/markdown/react.dev/reference/react/useState.md`.
    *   Explain `useState` based on that file's content.
```

**(Remember to adapt the base path in the rule if you use a custom `--output-dir`).**

By providing this rule, you guide the AI to use the most relevant, version-specific, and token-efficient documentation available directly within your project.

## Updating Documentation

Currently, updates require manually re-running the `mirror_docs.py` command for the specific documentation set. Future versions might include incremental update capabilities.

## Memory Bank 🧠

The `memory-bank/` directory contains documentation about this tool's design, implementation, and progress.

## License 📜

[MIT](LICENSE)

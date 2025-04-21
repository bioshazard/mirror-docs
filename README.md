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
uv run mirror_docs.py --domain <domain> --docs-path <docs_path> --output-dir <output_dir> --sitemap-file <sitemap_file>
```

**Arguments:**

*   `--domain`: The base domain URL (e.g., `https://react.dev`). Must include `http://` or `https://`.
*   `--docs-path`: The specific path on the domain containing the documentation (e.g., `/reference`). Start with `/`.
*   `--output-dir`: The local directory where the mirrored HTML (`html/`) and generated Markdown (`markdown/`) will be stored (e.g., `./.local_docs/react`). **It's recommended to add this directory to your project's `.gitignore` file.**
*   `--sitemap-file`: The path and name for the output sitemap file (e.g., `./.local_docs/react/sitemap.txt`). This file lists the relative paths to the generated Markdown files and their corresponding page titles.

**Example (Mirroring React Reference Docs):**

```bash
# Create a directory to hold the mirrored docs (and add it to .gitignore!)
mkdir -p .local_docs/react

# Run the tool
uv run mirror_docs.py \
    --domain https://react.dev \
    --docs-path /reference \
    --output-dir ./.local_docs/react \
    --sitemap-file ./.local_docs/react/sitemap.txt
```

This will:
1.  Mirror HTML content from `https://react.dev/reference` into `./.local_docs/react/html/`.
2.  Convert the main content of each HTML page into Markdown files within `./.local_docs/react/markdown/`.
3.  Generate a sitemap at `./.local_docs/react/sitemap.txt` listing the Markdown files and their titles like: `react/18/react/useState.md :: useState - React`

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

This project utilizes `mirror-docs` to maintain local copies of relevant framework/library documentation in the `.local_docs/` directory. Each subdirectory within `.local_docs/` corresponds to a mirrored site (e.g., `.local_docs/react/`) and contains:

*   `markdown/`: Directory with documentation converted to Markdown.
*   `sitemap.txt`: A file listing `relative/path/to/markdown.md :: Page Title`.

## Instruction

When I ask questions or request code related to a framework/library for which local documentation exists in `.local_docs/`:

1.  **Consult the Sitemap:** First, check the relevant `sitemap.txt` (e.g., `.local_docs/react/sitemap.txt`) to identify potentially relevant documentation pages based on their titles.
2.  **Read Local Markdown:** If relevant pages are found, prioritize reading the corresponding Markdown file(s) from the `markdown/` directory to gather context. Use the `read_file` tool with the path constructed by joining the `--output-dir` base and the relative path from the sitemap (e.g., `.local_docs/react/markdown/react/18/react/useState.md`).
3.  **Synthesize Answer:** Base your answer or code generation primarily on the information found in the local Markdown files.
4.  **Fallback:** If the necessary information isn't found locally, you may then resort to general knowledge or external searches, but state that the local docs were consulted first.

**Example Scenario:** If I ask "How do I use the `useState` hook in React?", you should:
    *   Look at `.local_docs/react/sitemap.txt`.
    *   Find the line like `react/18/react/useState.md :: useState - React`.
    *   Read the file `.local_docs/react/markdown/react/18/react/useState.md`.
    *   Explain `useState` based on that file's content.
```

**(Remember to adapt the paths in the rule to match your specific `--output-dir` structure).**

By providing this rule, you guide the AI to use the most relevant, version-specific, and token-efficient documentation available directly within your project.

## Updating Documentation

Currently, updates require manually re-running the `mirror_docs.py` command for the specific documentation set. Future versions might include incremental update capabilities.

## Memory Bank 🧠

The `memory-bank/` directory contains documentation about this tool's design, implementation, and progress.

## License 📜

[MIT](LICENSE) (Assuming MIT, create a LICENSE file if needed)

# Active Context: mirror-docs

## Current Work Focus

Refining the `mirror-docs` tool and documentation to position it as a solution for creating local, token-efficient documentation mirrors for AI assistant integration. Updating memory bank.

## Recent Changes

*   Updated `mirror_docs.py`:
    *   Added HTML `<title>` extraction using BeautifulSoup.
    *   Modified sitemap generation to include page titles (`path :: title` format).
    *   Added a `User-Agent` string to the `wget` command.
    *   Improved `wget` execution logging and error handling (allowing exit code 8).
    *   Fixed `ImportError` by removing the duplicate `main()` function and ensuring the correct one is called.
*   Added `beautifulsoup4` as an explicit dependency in `pyproject.toml`.
*   Added `mirror_docs.egg-info` to `.gitignore`.
*   Added classifiers to `pyproject.toml`.
*   Generated distribution packages using `uv build`.
*   Significantly updated `README.md` to reflect the new positioning, benefits, usage instructions, and provided an example `.clinerule` for AI integration.
*   Modified sitemap generation to be additive, merging entries from multiple mirrored sites.
*   Re-introduced `--include-directories` option to limit download scope.
*   Initialized the memory bank by reading all files.

## Next Steps

*   Update `progress.md` to reflect the current state.
*   Consider future enhancements (dependency checks, config file, incremental updates).
*   Test the script with diverse documentation sites.
*   Remove the old, now obsolete scripts (`00-mirror.sh`, `01-md.py`, `02-sitemap.sh`) if they still exist.
*   Update `pyproject.toml` if any new Python dependencies were added (BeautifulSoup was added implicitly via `readability-lxml`, but good to check).
*   Configured `pyproject.toml` for PyPI publishing.
*   Created GitHub Actions workflow for automated PyPI publishing using a PyPI token.

## Active Decisions and Considerations

*   How to best structure the mirrored documentation for optimal searchability and navigability.
*   Which data sources to prioritize for mirroring.

## Important Patterns and Preferences

*   Using Markdown for documentation.
*   Using Python for data acquisition and transformation.
*   Using shell scripts for automation.

## Learnings and Project Insights

*   The project has a clear separation of concerns between data acquisition, transformation, and presentation.
*   The use of shell scripts for automation simplifies the deployment and maintenance processes.

## TODO

- [X] Detect page Title to include in sitemap for easier LLM choice
- [ ] Reorganize sites to be modular and trickle up to multi-site
- [X] Update readme to point out token savings and call speed savings for online lookup (and AI integration)

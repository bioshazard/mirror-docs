# Active Context: mirror-docs

## Current Work Focus

Initializing the memory bank, documenting the existing codebase, and updating the documentation to reflect the project's intention and design.

## Recent Changes

*   Created the initial set of memory bank files: `projectbrief.md`, `productContext.md`, `systemPatterns.md`, and `techContext.md`.
*   Updated the memory bank to reflect the new plan of creating a generalized CLI tool.

## Next Steps

*   Create the `progress.md` file.
*   Develop the `mirror_docs.py` script.
*   Remove the old scripts (`00-mirror.sh`, `01-md.py`, `02-sitemap.sh`).
*   Update `pyproject.toml` if any new Python dependencies are required.

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

- [ ] Detect page Title to include in sitemap for easier LLM choice
- [ ] Reorganize sites to be modular and trickle up to multi-site
- [ ] Update readme to point out token savings and call speed savings for online lookup

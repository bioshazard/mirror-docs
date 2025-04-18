# System Patterns: mirror-docs

## System Architecture

The system follows a modular architecture, with distinct components for:

*   **Data Acquisition:** Scripts for fetching documentation from various sources (e.g., websites, APIs, file systems).
*   **Data Transformation:** Processes for converting documentation into a consistent format (e.g., Markdown).
*   **Storage:** A mechanism for storing the mirrored documentation (e.g., a file system, a database).
*   **Presentation:** A user interface for browsing and searching the documentation.

## Key Technical Decisions

*   **Markdown as the primary format:** Markdown was chosen for its simplicity, readability, and wide support.
*   **Python for scripting:** Python is used for data acquisition and transformation due to its rich ecosystem of libraries.
*   **Shell scripts for automation:** Shell scripts are used for automating tasks such as site generation and sitemap creation.

## Design Patterns

*   **Adapter Pattern:** Used to adapt different documentation sources to a common interface.
*   **Strategy Pattern:** Used to implement different transformation strategies for different documentation formats.

## Component Relationships

The data acquisition components feed data into the data transformation components, which then store the transformed data. The presentation layer retrieves data from the storage layer.

## Critical Implementation Paths

*   The `00-mirror.sh` script is responsible for mirroring raw HTML documentation from a specified domain.
*   The `01-md.py` script is responsible for converting the mirrored HTML to Markdown format.
*   The `02-sitemap.sh` script is responsible for generating the sitemap for indexing local full-docs references.

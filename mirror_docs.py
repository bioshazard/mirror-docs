import argparse
import os
import subprocess
# import requests
from bs4 import BeautifulSoup # Added for title extraction
from readability import Document
from markdownify import markdownify as md

def mirror_docs(domain, docs_path, output_dir, sitemap_file):
    """
    Mirrors HTML documentation from a specified domain and path,
    converts it to Markdown, and generates a sitemap file.
    """

    full_url = domain + docs_path
    html_output_dir = os.path.join(output_dir, "html")
    markdown_output_dir = os.path.join(output_dir, "markdown")

    os.makedirs(html_output_dir, exist_ok=True)
    os.makedirs(markdown_output_dir, exist_ok=True)

    # Mirror the HTML documentation using wget
    try:
        command = [
            "wget",
            "-q",
            "--mirror",
            "--convert-links",
            "--adjust-extension",
            "--page-requisites",
            "--no-parent",
            "--include-directories=" + docs_path,
            "--directory-prefix=" + html_output_dir,
            "--user-agent=mirror-docs/0.1", # Added User-Agent
            full_url,
        ]
        print(f"Running wget command: {' '.join(command)}") # Log the command
        result = subprocess.run(command, capture_output=True, text=True) # Capture output
        print(f"wget stdout:\n{result.stdout}")
        print(f"wget stderr:\n{result.stderr}")
        print(f"wget return code: {result.returncode}")
        # Allow code 8 (server errors like 404/5xx) as wget often returns this for minor issues during mirroring.
        if result.returncode == 0 or result.returncode == 8:
            print(f"Successfully mirrored HTML documentation from {full_url} (wget exit code: {result.returncode})")
        else:
            print(f"Error mirroring HTML documentation from {full_url}. wget exit code: {result.returncode}")
            print(f"stderr: {result.stderr}")
            # Consider whether to return or continue based on the error
            # return # Optional: uncomment to stop on critical wget errors
    except subprocess.CalledProcessError as e:
        print(f"Error executing wget: {e}")
        print(f"stderr: {e.stderr}")
        # return # Optional: uncomment to stop on critical wget errors
    except Exception as e: # Catch other potential errors like file system issues
        print(f"An unexpected error occurred during mirroring: {e}")
        # return # Optional: uncomment to stop

    # --- Conversion and Sitemap Generation ---
    sitemap_data = {} # Store path -> title mapping

    # Convert HTML to Markdown
    print("\n--- Starting HTML to Markdown Conversion ---")
    for root, _, files in os.walk(html_output_dir):
        for file in files:
            if file.endswith(".html"):
                html_path = os.path.join(root, file)
                try:
                    with open(html_path, "r", encoding="utf-8") as f:
                        html = f.read()

                    # Extract title using BeautifulSoup
                    soup = BeautifulSoup(html, 'html.parser')
                    page_title = soup.title.string.strip() if soup.title else "No Title Found"

                    # Use readability-lxml to extract the main content
                    doc = Document(html)
                    main_html = doc.summary()  # Extracted primary content as HTML

                    # Convert the HTML to Markdown
                    md_content = md(main_html)

                    # Determine output path
                    rel_path_dir = os.path.relpath(root, html_output_dir)
                    md_filename = os.path.splitext(file)[0] + ".md"
                    # Construct relative path for sitemap (relative to markdown_output_dir root)
                    # Example: if root is /output/html/subdir and file is page.html
                    # rel_path_dir = subdir
                    # md_filename = page.md
                    # rel_md_path = subdir/page.md
                    # Ensure forward slashes for consistency, handle '.' for root files
                    rel_md_path = os.path.join(rel_path_dir, md_filename).replace(os.path.sep, '/')
                    if rel_md_path.startswith('./'):
                        rel_md_path = rel_md_path[2:]


                    # Construct full path for writing the file
                    output_folder = os.path.join(markdown_output_dir, rel_path_dir)
                    os.makedirs(output_folder, exist_ok=True)
                    md_path = os.path.join(output_folder, md_filename) # Full path for writing

                    # Store data for sitemap (using relative path)
                    sitemap_data[rel_md_path] = page_title

                    with open(md_path, "w", encoding="utf-8") as f:
                        f.write(md_content)
                    print(f"Processed: {html_path} -> {md_path} (Title: {page_title})")
                except Exception as e:
                    print(f"Error processing file {html_path}: {e}")

    # Generate sitemap
    print("\n--- Generating Sitemap ---")
    try:
        with open(sitemap_file, "w", encoding="utf-8") as f:
            # Sort items by path for consistency
            for rel_md_path, title in sorted(sitemap_data.items()):
                # Ensure path uses forward slashes for consistency across OS
                f.write(f"{rel_md_path.replace(os.path.sep, '/')} :: {title}\n")
        print(f"Successfully generated sitemap file: {sitemap_file}")
    except Exception as e:
        print(f"Error writing sitemap file {sitemap_file}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Mirrors HTML documentation, converts it to Markdown, and generates a sitemap."
    )
    parser.add_argument("--domain", required=True, help="The base domain URL.")
    parser.add_argument(
        "--docs-path", required=True, help="The specific path on the domain containing the documentation."
    )
    parser.add_argument(
        "--output-dir", required=True, help="The local directory where the mirrored HTML and generated Markdown will be stored."
    )
    parser.add_argument(
        "--sitemap-file", required=True, help="The name of the output sitemap file."
    )

    args = parser.parse_args()

    mirror_docs(args.domain, args.docs_path, args.output_dir, args.sitemap_file)

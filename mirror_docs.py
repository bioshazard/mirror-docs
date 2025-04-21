import argparse
import os
import subprocess
from urllib.parse import urlparse
# import requests
from bs4 import BeautifulSoup # Added for title extraction
from readability import Document
from markdownify import markdownify as md

def mirror_docs(url, base_output_dir):
    """
    Mirrors HTML documentation from a specified domain and path,
    converts it to Markdown, and generates a sitemap file.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    docs_path = parsed_url.path # Includes leading slash if present

    # Ensure docs_path starts with a slash if it's not empty
    if docs_path and not docs_path.startswith('/'):
        docs_path = '/' + docs_path
    elif not docs_path:
        docs_path = '/' # Handle case where only domain is given

    # Define base directories for HTML and Markdown within the main output dir
    html_base_dir = os.path.join(base_output_dir, "html")
    markdown_base_dir = os.path.join(base_output_dir, "markdown")
    sitemap_file = os.path.join(base_output_dir, "sitemap.txt")

    # wget directory prefix should be the base HTML dir; wget creates domain/path inside it
    wget_output_prefix = html_base_dir

    # The actual directory where wget will place files for this specific domain/path
    html_content_dir = os.path.join(html_base_dir, domain) # We'll walk this later

    # Ensure base output directories exist
    os.makedirs(os.path.join(markdown_base_dir, domain), exist_ok=True) # Ensure domain dir exists in markdown too
    # No need to explicitly create html_content_dir, wget does that

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
            # Use docs_path directly. wget interprets it relative to the domain.
            # Need to handle the root path case carefully if docs_path is just '/'
            # Wget might need specific handling for root mirroring, but let's try this first.
            # If docs_path is '/', mirroring the whole domain might be too much.
            # Let's assume docs_path will usually be more specific.
            # Re-introduce scope limitation based on the parsed path
            "--include-directories=" + docs_path,
            "--directory-prefix=" + wget_output_prefix, # Base HTML dir
            "--user-agent=mirror-docs/0.1", # Added User-Agent
            url, # Use the full input URL
        ]
        print(f"Running wget command: {' '.join(command)}") # Log the command
        result = subprocess.run(command, capture_output=True, text=True, check=False) # Capture output, don't check=True yet
        print(f"wget stdout:\n{result.stdout}")
        print(f"wget stderr:\n{result.stderr}")
        print(f"wget return code: {result.returncode}")
        # Allow code 8 (server errors like 404/5xx) as wget often returns this for minor issues.
        if result.returncode not in (0, 8):
             print(f"Warning: wget command finished with exit code {result.returncode} for URL {url}")
             print(f"stderr: {result.stderr}")
             # Decide if we should stop. For now, let's continue to try processing what was downloaded.
        else:
             print(f"wget command finished for {url} (exit code: {result.returncode})")
    except Exception as e: # Catch other potential errors like file system issues
        print(f"An unexpected error occurred during mirroring: {e}")
        # return # Optional: uncomment to stop

    # --- Conversion and Sitemap Generation ---
    sitemap_data = {} # Store path -> title mapping

    # Convert HTML to Markdown
    print("\n--- Starting HTML to Markdown Conversion ---")
    # Walk the specific directory created by wget for this domain/path
    walk_target_html_dir = os.path.join(html_base_dir, domain)
    if not os.path.exists(walk_target_html_dir):
        print(f"Error: wget did not create the expected directory: {walk_target_html_dir}")
        return # Cannot proceed without the mirrored content

    for root, _, files in os.walk(walk_target_html_dir):
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

                    # Determine output path relative to the domain-specific HTML dir
                    rel_path_dir = os.path.relpath(root, walk_target_html_dir)
                    md_filename = os.path.splitext(file)[0] + ".md"

                    # Construct relative path for sitemap (relative to markdown_base_dir)
                    # Example: domain/rel_path_dir/md_filename
                    sitemap_rel_md_path = os.path.join(domain, rel_path_dir, md_filename).replace(os.path.sep, '/')
                    # Remove leading './' if present (e.g., if rel_path_dir is '.')
                    if sitemap_rel_md_path.startswith(f"{domain}/./"):
                         sitemap_rel_md_path = sitemap_rel_md_path.replace(f"{domain}/./", f"{domain}/", 1)


                    # Construct full path for writing the markdown file
                    output_folder = os.path.join(markdown_base_dir, domain, rel_path_dir)
                    os.makedirs(output_folder, exist_ok=True)
                    md_path = os.path.join(output_folder, md_filename) # Full path for writing

                    # Store data for sitemap (using the new relative path including domain)
                    sitemap_data[sitemap_rel_md_path] = page_title

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
        description="Mirrors HTML documentation from a URL, converts it to Markdown, and generates a sitemap."
    )
    parser.add_argument(
        "url",
        help="The full URL to the documentation path to mirror (e.g., https://react.dev/reference/rsc)."
    )
    parser.add_argument(
        "--output-dir",
        default=".mirror-docs",
        help="The local directory where mirrored content will be stored. Defaults to '.mirror-docs'."
    )

    args = parser.parse_args()

    # Basic URL validation
    if not urlparse(args.url).scheme or not urlparse(args.url).netloc:
        print(f"Error: Invalid URL provided: {args.url}")
        exit(1)

    mirror_docs(args.url, args.output_dir)

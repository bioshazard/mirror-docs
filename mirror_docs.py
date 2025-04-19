import argparse
import os
import subprocess
# import requests
from bs4 import BeautifulSoup
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
            full_url,
        ]
        result = subprocess.run(command)
        print(f"Return code: {result.returncode}")
        if result.returncode == 0:
            print(f"Successfully mirrored HTML documentation from {full_url}")
        else:
            print(f"Error mirroring HTML documentation from {full_url}, return code: {result.returncode}")
            # return
    except subprocess.CalledProcessError as e:
        print(f"Error mirroring HTML documentation: {e}")
        # return

    # Convert HTML to Markdown
    for root, _, files in os.walk(html_output_dir):
        for file in files:
            if file.endswith(".html"):
                html_path = os.path.join(root, file)
                try:
                    with open(html_path, "r", encoding="utf-8") as f:
                        html = f.read()

                    # Use readability-lxml to extract the main content
                    doc = Document(html)
                    main_html = doc.summary()  # Extracted primary content as HTML

                    # Convert the HTML to Markdown
                    md_content = md(main_html)

                    # Replicate the folder structure in the output directory
                    rel_path = os.path.relpath(root, html_output_dir)
                    output_folder = os.path.join(markdown_output_dir, rel_path)
                    os.makedirs(output_folder, exist_ok=True)
                    md_filename = os.path.splitext(file)[0] + ".md"
                    md_path = os.path.join(output_folder, md_filename)

                    with open(md_path, "w", encoding="utf-8") as f:
                        f.write(md_content)
                    print(f"Processed {html_path} -> {md_path}")
                except Exception as e:
                    print(f"Error processing {html_path}: {e}")

    # Generate sitemap
    with open(sitemap_file, "w", encoding="utf-8") as f:
        for root, _, files in os.walk(markdown_output_dir):
            for file in files:
                if file.endswith(".md"):
                    md_path = os.path.join(root, file)
                    f.write(md_path + "\n")
    print(f"Generated sitemap file: {sitemap_file}")


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

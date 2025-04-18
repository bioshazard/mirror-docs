import os
from readability import Document
from markdownify import markdownify as md

# Input directory containing downloaded HTML docs
input_dir = "www.instantdb.com/docs"
# Output directory for Markdown files
output_dir = "www.instantdb.com/docs_md"

for root, _, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.html'):
            html_path = os.path.join(root, file)
            with open(html_path, 'r', encoding='utf-8') as f:
                html = f.read()
            # Use readability-lxml to extract the main content
            doc = Document(html)
            main_html = doc.summary()  # Extracted primary content as HTML

            # Convert the HTML to Markdown
            md_content = md(main_html)

            # Replicate the folder structure in the output directory
            rel_path = os.path.relpath(root, input_dir)
            output_folder = os.path.join(output_dir, rel_path)
            os.makedirs(output_folder, exist_ok=True)
            md_filename = os.path.splitext(file)[0] + ".md"
            md_path = os.path.join(output_folder, md_filename)
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"Processed {html_path} -> {md_path}")

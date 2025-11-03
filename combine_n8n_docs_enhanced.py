#!/usr/bin/env python3
"""
Create an enhanced version with table of contents for Google Notebook LM
"""
import os
from pathlib import Path
from collections import defaultdict

def create_enhanced_docs():
    docs_dir = Path('docs')
    output_file = Path('../n8n_documentation_with_toc.md')

    # Find all markdown and mdx files
    md_files = sorted(list(docs_dir.rglob('*.md')) + list(docs_dir.rglob('*.mdx')))

    print(f"Found {len(md_files)} documentation files")

    # Organize files by category (top-level directory)
    categories = defaultdict(list)
    for file_path in md_files:
        rel_path = file_path.relative_to(docs_dir)
        parts = rel_path.parts
        if len(parts) > 1:
            category = parts[0]
        else:
            category = "root"
        categories[category].append((rel_path, file_path))

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write header
        outfile.write("# n8n Complete Documentation\n\n")
        outfile.write("**Source:** https://github.com/n8n-io/n8n-docs\n\n")
        outfile.write(f"**Total Files:** {len(md_files)}\n\n")
        outfile.write("**Date Compiled:** 2025-11-03\n\n")
        outfile.write("---\n\n")

        # Write table of contents
        outfile.write("## Table of Contents\n\n")
        for category in sorted(categories.keys()):
            outfile.write(f"### {category.upper()}\n\n")
            for rel_path, _ in categories[category]:
                # Create anchor link
                anchor = str(rel_path).replace('/', '-').replace('.', '-')
                outfile.write(f"- [{rel_path}](#{anchor})\n")
            outfile.write("\n")

        outfile.write("---\n\n")

        # Write all documents organized by category
        for category in sorted(categories.keys()):
            outfile.write(f"# {category.upper()}\n\n")

            for rel_path, file_path in categories[category]:
                try:
                    # Create anchor
                    anchor = str(rel_path).replace('/', '-').replace('.', '-')

                    # Write section header
                    outfile.write(f"\n## {rel_path}\n")
                    outfile.write(f"<a id=\"{anchor}\"></a>\n\n")

                    # Read and write file content
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write("\n\n")
                        outfile.write("---\n\n")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    outfile.write(f"*[ERROR: Could not read this file - {e}]*\n\n")

            print(f"Completed category: {category}")

    print(f"\nSuccessfully created enhanced documentation!")
    print(f"Output file: {output_file.absolute()}")

    # Get file size
    file_size = output_file.stat().st_size / (1024 * 1024)  # Convert to MB
    print(f"Output file size: {file_size:.2f} MB")

if __name__ == '__main__':
    create_enhanced_docs()

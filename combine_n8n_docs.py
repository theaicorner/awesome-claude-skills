#!/usr/bin/env python3
"""
Combine all n8n documentation files into a single file for Google Notebook LM
"""
import os
from pathlib import Path

def combine_docs():
    docs_dir = Path('docs')
    output_file = Path('../n8n_complete_documentation.txt')

    # Find all markdown and mdx files
    md_files = sorted(list(docs_dir.rglob('*.md')) + list(docs_dir.rglob('*.mdx')))

    print(f"Found {len(md_files)} documentation files")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Write header
        outfile.write("=" * 80 + "\n")
        outfile.write("n8n COMPLETE DOCUMENTATION\n")
        outfile.write("Compiled from: https://github.com/n8n-io/n8n-docs\n")
        outfile.write(f"Total files: {len(md_files)}\n")
        outfile.write("=" * 80 + "\n\n")

        # Process each file
        for idx, file_path in enumerate(md_files, 1):
            try:
                # Get relative path for context
                rel_path = file_path.relative_to(docs_dir)

                # Write section header
                outfile.write("\n" + "=" * 80 + "\n")
                outfile.write(f"FILE {idx}/{len(md_files)}: {rel_path}\n")
                outfile.write("=" * 80 + "\n\n")

                # Read and write file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                    content = infile.read()
                    outfile.write(content)
                    outfile.write("\n\n")

                if idx % 100 == 0:
                    print(f"Processed {idx}/{len(md_files)} files...")

            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                outfile.write(f"\n[ERROR: Could not read this file - {e}]\n\n")

    print(f"\nSuccessfully combined all documentation!")
    print(f"Output file: {output_file.absolute()}")

    # Get file size
    file_size = output_file.stat().st_size / (1024 * 1024)  # Convert to MB
    print(f"Output file size: {file_size:.2f} MB")

if __name__ == '__main__':
    combine_docs()

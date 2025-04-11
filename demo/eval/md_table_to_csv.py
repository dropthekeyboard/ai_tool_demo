#!/usr/bin/env python3
"""
Markdown Table to CSV Converter

This script extracts tables from markdown files and converts them to CSV format.
Usage: python md_table_to_csv.py <input_markdown_file> <output_csv_file>
"""

import sys
import os
import re
import csv

def extract_table_from_markdown(markdown_file):
    """Extract table rows from a markdown file."""
    with open(markdown_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extract the table section
    table_section_pattern = r'## 평가 결과 요약표\s*\n\n(.*?)(?:\n\n|\n##|\Z)'
    table_section_match = re.search(table_section_pattern, content, re.DOTALL)
    
    if not table_section_match:
        print("Table section not found in the markdown file.")
        return None
    
    table_content = table_section_match.group(1)
    
    # Extract header row
    lines = table_content.strip().split('\n')
    if len(lines) < 3:  # Need at least header, separator, and one data row
        print("Not enough lines for a table.")
        return None
    
    # Extract headers
    header_line = lines[0]
    header_match = re.match(r'\|(.*)\|', header_line)
    if not header_match:
        print("Header line not properly formatted.")
        return None
    
    header_cells = [cell.strip() for cell in header_match.group(1).split('|')]
    
    # Skip the separator line (line[1]) and process data rows
    data_rows = []
    for i in range(2, len(lines)):
        row_match = re.match(r'\|(.*)\|', lines[i])
        if row_match:
            cells = [cell.strip() for cell in row_match.group(1).split('|')]
            if len(cells) == len(header_cells):
                data_rows.append(cells)
    
    return header_cells, data_rows

def write_to_csv(header, rows, output_file):
    """Write the extracted table data to a CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"CSV file created: {output_file}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python md_table_to_csv.py <input_markdown_file> <output_csv_file>")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(markdown_file):
        print(f"Error: File {markdown_file} not found.")
        sys.exit(1)
    
    table_data = extract_table_from_markdown(markdown_file)
    
    if table_data:
        header, rows = table_data
        write_to_csv(header, rows, output_file)
    else:
        print("No table found or error in processing the markdown file.")
        sys.exit(1)

if __name__ == "__main__":
    main() 
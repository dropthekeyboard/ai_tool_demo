import csv
import re

def extract_markdown_table_to_csv(markdown_file_path, csv_file_path):
    """
    Reads a Markdown file, extracts the first table found,
    and writes its content to a CSV file.

    Args:
        markdown_file_path (str): Path to the input Markdown file.
        csv_file_path (str): Path to the output CSV file.
    """
    try:
        with open(markdown_file_path, 'r', encoding='utf-8') as md_file:
            lines = md_file.readlines()

        table_lines = []
        in_table = False
        header_found = False
        separator_found = False

        # Find the table lines
        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith('|') and stripped_line.endswith('|'):
                if not in_table:
                    in_table = True
                table_lines.append(stripped_line)
                # Basic check for separator line (contains '---')
                if '---' in stripped_line:
                    separator_found = True
                elif separator_found: # Lines after the separator are data
                    header_found = True # Assume header is the line before separator

            elif in_table: # If we were in a table and hit a non-table line, stop
                break

        if not table_lines or len(table_lines) < 3: # Need header, separator, and at least one data row
            print(f"No valid Markdown table found in {markdown_file_path}")
            return

        # Extract header and data rows
        header_line = table_lines[0]
        data_lines = table_lines[2:] # Skip header and separator

        # Function to parse a table row
        def parse_table_row(line):
            # Remove leading/trailing '|' and split by '|'
            # Strip whitespace from each cell
            return [cell.strip() for cell in line.strip('|').split('|')]

        header = parse_table_row(header_line)
        data = [parse_table_row(line) for line in data_lines]

        # Write to CSV
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(data)

        print(f"Successfully extracted table from {markdown_file_path} to {csv_file_path}")

    except FileNotFoundError:
        print(f"Error: File not found at {markdown_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Script Execution ---
markdown_input_file = 'demo/eval/eval_by_gemini_2_5.md'
csv_output_file = 'evaluation_results.csv'

extract_markdown_table_to_csv(markdown_input_file, csv_output_file)

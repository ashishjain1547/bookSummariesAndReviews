import csv

def format_csv_to_text(input_file, output_file):
    """
    Reads a CSV with columns 'title', 'author', 'year'
    and writes a formatted text file.
    """
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        for idx, row in enumerate(reader, start=1):
            # Extract fields, strip any surrounding whitespace
            title = row.get('title', '').strip()
            author = row.get('author', '').strip()
            year = row.get('year', '').strip()

            # Write formatted block
            outfile.write(f"{idx}\n")
            outfile.write(f"{title}\n")
            outfile.write(f"By: {author}\n")
            outfile.write(f"Year Published: {year}\n")
            outfile.write("<br/>\n")

if __name__ == "__main__":
    input_csv = "input.csv"    # Change to your CSV file path
    output_txt = "output.txt"  # Desired output path
    try:
        format_csv_to_text(input_csv, output_txt)
        print(f"Formatted data written to {output_txt}")
    except FileNotFoundError:
        print(f"Error: file '{input_csv}' not found.")
    except KeyError as e:
        print(f"Error: missing expected column in CSV – {e}")
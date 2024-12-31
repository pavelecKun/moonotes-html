# Required to parse arguments
import argparse
from datetime import datetime, timezone
from operator import itemgetter

# Required to create and manipulate HTML file
import jinja2
from titlecase import titlecase

# Required to encode image into HTML file
import base64
import os

# Function to encode cover.png image into HTML base64 format
def image_encode():
    if os.path.exists("./cover.png"):
        with open("./cover.png", "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    else:
        return ""  # Return an empty string if cover.png is not found

DATETIMESTR = ''.join(
    [ch for ch in datetime.now(timezone.utc).isoformat()[0:19] if ch.isdigit()])

def capitalize_title(ugly_title):
    if (all(ch.isupper() or not(ch.isalpha()) for ch in ugly_title) or
            all(ch.islower() or not(ch.isalpha()) for ch in ugly_title)):
        # Title is ugly, titlecase it
        return titlecase(ugly_title)
    else:
        return ugly_title

def capitalize_headings(highlights):
    for highlight in highlights:
        if highlight['note'] and highlight['note'].startswith('.h'):
            highlight['text'] = capitalize_title(highlight['text'])

# Function to load Jinja Template
def load_template():
    return jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="./")).get_template("output.j2")

# Function to add break for each highlight
def fix_highlight_text(unfixed):
    return unfixed.replace('<BR>', '\n')

# Function to get color of highlight from .mrexpt
def get_color(color_code):
    return (str(hex(4294967295 + int(color_code) + 1))[4:])

# Function to remove duplicate highlights
def remove_duplicate_highlights(full_highlights):
    unique_highlights = []
    for full_highlight in full_highlights:
        if len(unique_highlights) > 0:
            if (unique_highlights[-1]['text'] == full_highlight['text'] and
                    unique_highlights[-1]['note'] == full_highlight['note']):
                continue
        unique_highlights.append(full_highlight)
    return unique_highlights

# Function to handle encoding errors
def read_file_with_fallback(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            return file.read().splitlines()
    except UnicodeDecodeError:
        print(f"Warning: UTF-8 decoding failed for {filename}. Trying with latin-1.")
        with open(filename, 'r', encoding="latin-1") as file:
            return file.read().splitlines()

def do_convert(mrexpt_filename, html_filename, debug=True, titlecap=True,
               book_name=None, author='Unknown'):
    items = []

    # Read the file with fallback for encoding issues
    lines = read_file_with_fallback(mrexpt_filename)
    current_item = []
    for line in lines:
        # A line with `#` starts a new item
        if line == '#':
            items.append(current_item)
            current_item = []
        else:
            # Each line is a field
            current_item.append(line)
    items.append(current_item)

    if book_name is None:
        # The book name and filename is present in every highlight, so pick it up from the first
        book_name = items[1][1] or items[1][2]
    if debug:
        book_name = book_name + ' - ' + DATETIMESTR
    # The first item isn't a highlight, it's some obscure metadata, so drop it
    items = items[1:]
    # print(items)

    highlights = [
        {
            # No absolute location, so take the chapter number times million and add the location in the chapter
            # Note is empty for highlights without a note
            'color': get_color(item[8]),
            'text': fix_highlight_text(item[12]),
            'note': item[11],
            'location': (int(item[4]) * 1000000) + int(item[6]),

        }
        for item in items
    ]
    # The .mrexpt is ordered by note creation, so now that we have an approximate location sort by that
    highlights = remove_duplicate_highlights(
        sorted(highlights, key=itemgetter('location')))
    if titlecap:
        capitalize_headings(highlights)

    # Rendering highlights for Jinja file
    render_vars = {
        'author': author,
        'highlights': highlights,
        'image': image_encode(),  # Use the image_encode function
    }
    # Writing HTML File
    with open(html_filename, 'w', encoding="utf-8") as html_file:
        html_file.write(load_template().render(render_vars))


def boolstr(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 'on', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'off', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Function for parsing arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input file")
    parser.add_argument("-d", "--debug", type=boolstr, default=True,
                        help="run in debug mode - unique file and book name")
    parser.add_argument("-t", "--titlecap", type=boolstr, default=True,
                        help="convert ALL CAPS headings to Title Cap")
    parser.add_argument("-a", "--author", type=str,
                        help="name of the author(s)",
                        default='Unknown')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    mrexpt_filename = args.input
    html_filename = mrexpt_filename.replace('mrexpt', 'html')
    if args.debug:
        html_filename = html_filename.replace(
            '.html', '-' + DATETIMESTR + '.html')

    do_convert(mrexpt_filename, html_filename, debug=args.debug, titlecap=args.titlecap, author=args.author)

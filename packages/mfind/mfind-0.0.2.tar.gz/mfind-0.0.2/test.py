from mfind import MultiFinder
from eprint import eprint


def internal_handler(filename: str):
    return False    # Just about all other handler checks


def html_handler(filename: str):
    eprint.ok("Processing HTML file {}", filename)


def mardkown_handler(filename: str):
    eprint.ok("Processing markdown file {}", filename)


file_processing_map = {
    "_*" : internal_handler,
    "*.html" : html_handler,
    "*.md" : mardkown_handler
}

mf = MultiFinder(file_processing_map)
mf.scan("test_dir", filename_only_match=True)

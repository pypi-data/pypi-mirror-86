# mfind

The mfind library allows to scan a directory for file an apply callbacks on file matches

# How to install

```sh
pip install mfind
```

# How to use

```python
from mfind import MultiFinder

def internal_handler(filename: str):
    return False    # Just about all other handler checks


def html_handler(filename: str):
    print(f"Processing HTML file {filename}")


def mardkown_handler(filename: str):
    print(f"Processing markdown file {filename}")


file_processing_map = {
    "_*" : internal_handler,
    "*.html" : html_handler,
    "*.md" : mardkown_handler
}

mf = MultiFinder(file_processing_map)
mf.scan("test_dir", filename_only_match=True)
```
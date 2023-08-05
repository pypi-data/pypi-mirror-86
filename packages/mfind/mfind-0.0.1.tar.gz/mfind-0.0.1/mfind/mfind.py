from fnmatch import fnmatch
from os import scandir
from pathlib import Path


class MultiFinder:

    def __init__(self, processor_map: dict):
        self._processor_map = processor_map

    def scan(self, path: str, filename_only_match: bool = False):
        for entry in scandir(path):
            if filename_only_match and not entry.is_file:
                continue
            match_element = Path(entry.name)
            if filename_only_match:
                match_element = match_element.name
            for proc_mask, proc_func in self._processor_map.items():
                if fnmatch(match_element, proc_mask):
                    if proc_func(match_element) is False:
                        break

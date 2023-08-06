import argparse
import pathlib
import re
import sys
from collections import OrderedDict
from io import TextIOBase
from typing import List


class LineMultiplexer:
    def __init__(self):
        self.output = pathlib.Path("linemux")
        self.key = ".+"
        self.remove_key = False
        self.max_files_open = 256
        self.max_lines = -1
        self.max_name_length = 128

    def process(self, in_stream: TextIOBase):
        """Process the given stream"""
        self.output.mkdir(parents=True,exist_ok=True)

        filter = re.compile(r"[^-_.a-zA-Z0-9]")
        pattern = re.compile(self.key or ".+")

        file_cache = OrderedDict()

        line = in_stream.readline()
        files = {}
        line_count = 0
        while line and (self.max_lines == -1 or line_count < self.max_lines):
            line_key = pattern.match(line)
            line_count += 1
            if not line_key:
                line = in_stream.readline()
                continue
            key_name = line_key.group(0)
            if key_name not in files:
                base_name = filter.sub('', key_name)
                file_name = base_name[:self.max_name_length]
                count = 1
                out_file = self.output / file_name
                while out_file.exists():
                    # naming conflict
                    count += 1
                    count_s = f"_{count}"
                    cut_base_to = max(0, self.max_name_length - len(count_s))
                    file_name = base_name[:cut_base_to] + count_s
                    out_file = self.output / file_name
                print(file_name)
                files[key_name] = file_name
            else:
                file_name = files[key_name]
                out_file = self.output / file_name

            file = file_cache.pop(file_name, None)
            if file:
                # in cache
                file_cache[file_name] = file
            else:
                # open new file
                while len(file_cache) > self.max_files_open:
                    # close oldest file
                    _, remove = file_cache.popitem(last=False)
                    remove.close()
                out_file = self.output / file_name
                file = out_file.open('a')
                file_cache[file_name] = file
            write_line = line
            if self.remove_key:
                write_line = line[len(key_name):]
            file.write(write_line)

            line = in_stream.readline()
        # close open files
        for file in file_cache.values():
            file.close()


def main(args: List[str] = None):
    m_parser = argparse.ArgumentParser()
    m_parser.add_argument("-d", "--output-dir", nargs='?',
                          help="Output directory (default 'linemux')")
    m_parser.add_argument("-k", "--key", nargs='?',
                          help="Key regexp (default '.+' for the whole line)")
    m_parser.add_argument("-K", "--remove-key", action='store_true',
                          help="Remove key from written value")
    m_parser.add_argument("--max-name-length", '-L', type=int, nargs='?',
                          help="Maximum file name length (default 128)")
    m_parser.add_argument("--max-files-open", type=int, nargs='?',
                          help="How many files max. kept open simultaneously (default 256)")
    m_parser.add_argument("--max-lines", type=int, nargs='?',
                          help="Process maximum of given lines (nice for testing)")
    m_parser.add_argument("file", nargs="?",
                          help="File to process")

    args = m_parser.parse_args(sys.argv[1:] if args is None else args)
    mux = LineMultiplexer()
    if args.output_dir:
        mux.output = pathlib.Path(args.output_dir)
    if args.key:
        mux.key = args.key
    if args.remove_key:
        mux.remove_key = True
    if args.max_name_length:
        mux.max_name_length = args.max_name_length
    if args.max_files_open:
        mux.max_files_open = args.max_files_open
    if args.max_lines:
        args.max_lines = args.max_lines
    in_stream = sys.stdin
    if args.file:
        in_stream = pathlib.Path(args.file).open("r")
    mux.process(in_stream)

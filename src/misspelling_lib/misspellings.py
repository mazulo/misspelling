#!/usr/bin/env python
"""
Checks files against a list of commonly misspelled words.

Wikipedia contains a large number of proper nouns and technical
terms. Traditional spell-checking in this case is problematic.
Instead, it has a page that people can use to list commonly misspelled
words and to then use that to find misspellings.

A similar approach can be taken to spell-checking (or misspell-checking)
the files in a body of source code.

This tool uses the English wordlist from Wikipedia in order to scan
source code and identify misspelled words.
"""

import codecs
import signal
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console

file = Path(__file__).resolve()
package_root_directory = file.parent.parent
sys.path.append(str(package_root_directory))


from misspelling_lib import MisspellingFactory
from misspelling_lib.utils import MisspellingArgumentParser, expand_directories, get_version, parse_file_list


def entrypoint() -> Optional[int]:
    """Internal main entry point."""
    parser = MisspellingArgumentParser()
    args = parser.parse_args()

    if args.file_list:
        try:
            args.files += parse_file_list(args.file_list)
        except IOError as exception:
            parser.error(exception)

    output = codecs.getwriter("utf-8")(sys.stdout.buffer if hasattr(sys.stdout, "buffer") else sys.stdout)

    if args.version:
        console = Console()
        console.print(f"[green]misspellings version[/green]: [bold green]{get_version()}")
        return 0

    if args.misspelling_file:
        misspelling = MisspellingFactory.factory(
            misspelling_detector_name="misspelling_file_detector",
            misspelling_file=args.misspelling_file,
        )
        args.files = expand_directories(args.files)

        if args.export_file:
            with open(args.export_file, "w", encoding="utf-8") as correction_file:
                misspelling.export_result_to_file(filenames=args.files, output=correction_file)
    elif args.json_file:
        misspelling = MisspellingFactory.factory(
            misspelling_detector_name="misspelling_json_detector",
            misspelling_file=args.json_file,
        )
        args.files = expand_directories(args.files)

        if args.export_file:
            with open(args.export_file, "w", encoding="utf-8") as correction_file:
                misspelling.export_result_to_file(filenames=args.files, output=correction_file)
    else:
        misspelling = MisspellingFactory.factory(misspelling_detector_name="misspelling_detector")
        args.files = expand_directories(args.files)

        if args.export_file:
            with open(args.export_file, "w", encoding="utf-8") as correction_file:
                misspelling.export_result_to_file(filenames=args.files, output=correction_file)

    if args.dump_misspelling:
        for word, correction in misspelling.dump_corrections():
            output.write("%s %s\n" % (word, correction))

    if args.script_output:
        misspelling.output_sed_commands(parser, args, filenames=args.files)
    else:
        return 2 if misspelling.print_result(filenames=args.files, output=output) else 0


def main():
    """Main entry point"""
    try:
        # Exit on broken pipe.
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass

    try:
        return entrypoint()
    except KeyboardInterrupt:
        return 2


if __name__ == "__main__":
    sys.exit(main())

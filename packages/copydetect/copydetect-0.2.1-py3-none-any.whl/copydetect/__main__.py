from .detector import CopyDetector
from . import __version__
import numpy as np
import os
import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser(prog="copydetect",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--conf", metavar="CONFIGURATION.JSON",
                        help="path to the JSON configuration file, if "
                        "using file configuration rather than command "
                        "line flags")
    parser.add_argument("-t", "--test-dirs", nargs='+',
                        metavar="TEST-DIRECTORY",
                        help="list of directories to recursively search for "
                             "files to check for plagairism")
    parser.add_argument("-r", "--ref-dirs", nargs='+',
                        metavar="REFERENCE-DIRECTORY",
                        help="list of directories to recursively search for "
                        "files to compare the test files to. If left empty, "
                        "the test directories themselves are used")
    parser.add_argument("-b", "--boilerplate-dirs", nargs='+',
                        metavar="BOILERPLATE-DIRECTORY", default=[],
                        help="list of directories to recursively search for "
                        "files containing boilerplate code")
    parser.add_argument("-e", "--extensions", nargs='+', default=["*"],
                        metavar="EXTENSIONS",
                        help="list of file extensions to collect code from")
    parser.add_argument("-n", "--noise-thresh", default=25, type=int,
                        metavar="NOISE-THRESHOLD",
                        help="length of minimum number of matching characters "
                        "which should be considered copied")
    parser.add_argument("-g", "--guarantee-thresh", default=30, type=int,
                        metavar="GUARANTEE-THRESHOLD",
                        help="length of minimum number of matching characters "
                        "which the parser is guaranteed to detect as copied")
    parser.add_argument("-d", "--display-thresh", default=.33, type=float,
                        metavar="DISPLAY-THRESHOLD",
                        help="percentage of copied code considered interesting"
                        " enough to display on the report")
    parser.add_argument("-o", '--force-language', dest='language',
                        default=None,
                        help="language to use for tokenization (if not "
                        "provided, the tokenizer guesses based on file "
                        "extensions)")
    parser.add_argument("-s", '--same-name', dest='same_name',
                        action='store_true', default=False,
                        help="only compare files which have the same name")
    parser.add_argument("-l", '--ignore-leaf', dest='ignore_leaf',
                        action='store_true', default=False,
                        help="don't compare files located in the same "
                        "leaf directory")
    parser.add_argument("-f", '--disable-filter', dest='filter',
                        action='store_true', default=False,
                        help="disable code tokenization and filtering")
    parser.add_argument("-a", '--disable-autoopen', dest='autoopen',
                        action='store_true', default=False,
                        help="disable browser autoopen")
    parser.add_argument("-T", '--truncate', dest='truncate',
                        action='store_true', default=False,
                        help="truncate non-copied portions of highlighted "
                        "code")
    parser.add_argument('--version', action='version',
                        version="copydetect v" + __version__,
                        help="print version number and exit")
    args = parser.parse_args()

    if args.conf:
        with open(args.conf) as json_fp:
            config = json.load(json_fp)
    elif args.test_dirs:
        if not args.ref_dirs:
            args.ref_dirs = args.test_dirs
        config = {
          "test_directories" : args.test_dirs,
          "reference_directories" : args.ref_dirs,
          "boilerplate_directories" : args.boilerplate_dirs,
          "extensions" : args.extensions,
          "noise_threshold" : args.noise_thresh,
          "guarantee_threshold" : args.guarantee_thresh,
          "display_threshold" : args.display_thresh,
          "force_language" : args.language,
          "same_name_only" : args.same_name,
          "ignore_leaf" : args.ignore_leaf,
          "disable_filtering" : args.filter,
          "disable_autoopen" : args.autoopen,
          "truncate" : args.truncate,
        }
    else:
        parser.error("either a path to a configuration file (-c) or a "
                     "list of test directories (-t) must be provided.")

    # get overlapping code
    detector = CopyDetector(config)
    detector.run()
    detector.generate_html_report("report", "report")

if __name__ == "__main__":
    main()

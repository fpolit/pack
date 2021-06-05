#!/usr/bin/env python3
#
# statsgen command line
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
import sys

from typing import List
import argparse
from fineprint.status import print_failure


from ..statsgen import StatsGen
from ..banner import statsgen_banner

def statsgen_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("wordlist",
                        help="Wordlist File")
    parser.add_argument("-o", "--output", default=None,
                        help="Output File")
    parser.add_argument("--minlength", type=int, default=None,
                        help="Minimum password length")
    parser.add_argument("--maxlength", type=int, default=None,
                        help="Maximum password length")
    parser.add_argument("--simplemasks", type=str, nargs='*', default=None,
                        help="Types of mask structures")
    parser.add_argument("--charsets", type=str, nargs='*', default=None,
                        help="Types of charset of password")
    parser.add_argument("-q", "--quiet", action='store_true',
                        help="Run quietly")
    parser.add_argument("-r", "--hiderare", type=int, default=0,
                        help="Hide statistics with lower rate")

    return parser

def statsgen(*, wordlist: str, output: str = None,
             min_length:int = None, max_length: int = None,
             simple_masks: List[str] = None, charsets: List[str] = None,
             quiet: bool = True, hiderare: int = 0):

    #import pdb; pdb.set_trace()
    try:
        if not (os.path.isfile(wordlist) and os.access(wordlist, os.R_OK)):
            if not os.path.isfile(wordlist):
                raise FileExistsError(f"File {wordlist} didn't exist.")
            else:
                raise PermissionError(f"No read permission in {wordlist} file")

        statsgen = StatsGen(wordlist = wordlist,
                            output = output,
                            minlength = min_length,
                            maxlength = max_length,
                            simplemasks = simple_masks,
                            charsets = charsets,
                            quiet = quiet,
                            hiderare = hiderare)


        if not quiet:
            print(statsgen_banner())

        print(f"[*] Analyzing passwords in {wordlist}")

        statsgen.generate_stats()
        statsgen.print_stats()

    except Exception as error:
        print_failure(error)

def main():
    parser = statsgen_parser()
    args = parser.parse_args()

    statsgen(wordlist = args.wordlist,
             min_length = args.minlength,
             max_length = args.maxlength,
             charsets = args.charsets,
             simple_masks = args.simplemasks,
             output = args.output,
             hiderare = args.hiderare,
             quiet = args.quiet)

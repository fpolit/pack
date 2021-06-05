#!/usr/bin/env python3
#
# wholegen - Perform a full analysis (statsgen and maskgen) to a wordlist and generate masks
#
# Status: DEBUGGED - date Jun 5 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import os
from typing import List
import sys
import re, operator, string
import time
import datetime
from operator import itemgetter
from math import floor


from .version import pack_version

from .statsgen import StatsGen
from .maskgen import MaskGen

class WholeGen:
    """
    Perform a full analysis (statsgen and maskgen) to a wordlist and generate masks
    """

    VERSION = pack_version()
    banner  = "                       _ \n"
    banner += "     WholeGen  %s  | |\n"  % VERSION
    banner += "      _ __   __ _  ___| | _\n"
    banner += "     | '_ \ / _` |/ __| |/ /\n"
    banner += "     | |_) | (_| | (__|   < \n"
    banner += "     | .__/ \__,_|\___|_|\_\\\n"
    banner += "     | |                    \n"
    banner += "     |_| iphelix@thesprawl.org\n"
    banner += "\n"

    def __init__(self, *,
                 #files
                 wordlist: str, output: str,
                 #filters
                 simplemasks: List[str] = None, charsets: List[str] = None,
                 minlength: int      = None, maxlength: int    = None,
                 mindigit:int        = None, maxdigit:int      = None,
                 minupper:int        = None, maxupper:int      = None,
                 minlower:int        = None, maxlower:int      = None,
                 minspecial:int      = None, maxspecial:int    = None,
                 mincomplexity:int   = None, maxcomplexity:int = None,
                 minoccurrence:int   = None, maxoccurrence:int = None,
                 target_time:int     = None, mintime:int       = None, maxtime:int       = None,
                 check_masks: List[str] = None, check_masks_file: str = None,
                 hiderare: int       = 0,

                 #print
                 showmasks:bool = False, quiet: bool = False):


        self.quiet = quiet
        self.wordlist = wordlist
        self.statsgen_output = os.path.basename(output) + ".stats"
        self.output = output
        self.check_masks = check_masks
        self.check_masks_file = check_masks_file


        self.statsgen = StatsGen(wordlist = wordlist,
                                 output = self.statsgen_output,
                                 minlength = minlength,
                                 maxlength = maxlength,
                                 simplemasks = simplemasks,
                                 charsets = charsets,
                                 quiet = quiet,
                                 hiderare = hiderare)

        self.maskgen = MaskGen(target_time = target_time,
                               output_file = output,
                               minlength = minlength,
                               maxlength = maxlength,
                               mintime = mintime,
                               maxtime = maxtime,
                               mincomplexity = mincomplexity,
                               maxcomplexity = maxcomplexity,
                               minoccurrence = minoccurrence,
                               maxoccurrence = maxoccurrence,
                               showmasks = showmasks)

    def full_analysis(self, sorting_mode):

        # StatsGen
        if not self.quiet:
            print(WholeGen.banner)

        print(f"[*] Analyzing passwords in {self.wordlist}")

        self.statsgen.generate_stats()
        self.statsgen.print_stats()

        print(f"[*]\n[+] Stats were saved in {self.statsgen_output}")

        # Maskgen
        print("[*]")
        print(f"[*] Analyzing masks in {self.statsgen_output}")
        pps = 1000000000

        print("[*] Using {:,d} keys/sec for calculations.".format(pps))

        # Load masks
        self.maskgen.loadmasks(self.statsgen_output)

        # Matching masks from the command-line
        if self.check_masks:
            print(f"[*] Checking coverage of the these masks [{', '.join(self.check_masks)}]")
            self.maskgen.getmaskscoverage(self.check_masks)

        elif self.check_masks_file:
            checkmasksfile = open(self.check_masks_file, 'r')
            print("[*] Checking coverage of masks in [%s]" % self.check_masks_file)
            self.maskgen.getmaskscoverage(self.checkmasksfile)

        else:# Printing masks in a file
            print("[*] Sorting masks by their [%s]." % sorting_mode)
            self.maskgen.generate_masks(sorting_mode)

        if self.output:
            print(f"[+] Masks were saved in {self.output}")


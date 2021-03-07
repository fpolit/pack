#!/usr/bin/env python3

from fineprint.status import print_failure

from typing import List

from pack_ama import StatsGen

from pack_ama.banner import (
    statsgen_banner,
    maskgen_banner,
    policygen_banner
)


def statsgen(*, wordlist: str, output: str = None,
             min_length:int = None, max_length: int = None,
             simple_masks: List[str] = None, charsets: List[str] = None,
             quiet: bool = True, hiderare: bool = False):

    import pdb; pdb.set_trace()
    try:
        #permission = [os.R_OK]
        #Path.access(permission, wordlist)
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

        if output:
            print(f"[*] Saving advanced masks and occurrences to {output}")

        statsgen.generate_stats()
        statsgen.print_stats()

    except Exception as error:
        print_failure(error)


if __name__=="__main__":
    wordlist = "wl/john.txt"
    output = "john.masks"
    statsgen(wordlist=wordlist,
             output = output,
             quiet=False)

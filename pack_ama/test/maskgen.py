#!/usr/bin/env python3

from fineprint.status import print_failure

from typing import List

from pack_ama import MaskGen

from pack_ama.banner import (
    statsgen_banner,
    maskgen_banner,
    policygen_banner
)


def maskgen(*,
            statsgen_output: str, output: str,
            min_length: int = None, max_length: int = None,
            target_time: int = None, min_time:int = None, max_time:int = None,
            min_complexity: int = None, max_complexity: int = None,
            min_occurrence: int = None, max_occurrence: int = None,
            sorting:str = "optindex",
            check_masks: List[str] = None, check_masks_file: str = None,
            show_masks: bool = False, quiet: bool = True):

    import pdb; pdb.set_trace()
    try:
        #permission = [os.R_OK]
        #Path.access(permission, statsgen_output)

        if not quiet:
            print(Pack.MASKGEN_BANNER)


        print(f"[*] Analyzing masks in {statsgen_output}")
        pps = 1000000000
        maskgen = MaskGen(
            target_time = target_time,
            output_file = output,
            minlength = min_length,
            maxlength = max_length,
            mintime = min_time,
            maxtime = max_time,
            mincomplexity = min_complexity,
            maxcomplexity = max_complexity,
            minoccurrence = min_occurrence,
            maxoccurrence = max_occurrence,
            pps = pps,
            showmasks = show_masks)

        # Settings
        if output:
            print(f"[*] Saving generated masks to {output}")

        print("[*] Using {:,d} keys/sec for calculations.".format(pps))

        # Load masks
        maskgen.loadmasks(statsgen_output)

        # Matching masks from the command-line
        if check_masks:
            print(f"[*] Checking coverage of the these masks [{', '.join(check_masks)}]")
            maskgen.getmaskscoverage(check_masks)

        # Matching masks from a file
        elif check_masks_file:
            checkmasksfile = open(check_masks_file, 'r')
            print("[*] Checking coverage of masks in [%s]" % check_masks_file)
            maskgen.getmaskscoverage(checkmasksfile)

        else:# Printing masks in a file
            print("[*] Sorting masks by their [%s]." % sorting)
            maskgen.generate_masks(sorting)

    except Exception as error:
        print_failure(error)


if __name__=="__main__":
    statsgen_output = "john.masks"
    output = "john.hcmasks"
    show_masks = True
    min_length = 4
    max_length = 6


    maskgen(statsgen_output= statsgen_output,
            output=output,
            show_masks=show_masks,
            min_length=min_length,
            max_length = max_length)

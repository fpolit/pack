#!/usr/bin/env python3

from fineprint.status import print_failure

from typing import List

from pack_ama import PolicyGen

from pack_ama.banner import (
    statsgen_banner,
    maskgen_banner,
    policygen_banner
)


def policygen( *,
               output: str = None,
               min_length:int = None, max_length:int = None, min_digit:int = None, max_digit: int = None,
               min_upper:int = None, max_upper:int = None, min_lower:int = None, max_lower:int = None,
               min_special:int = None, max_special:int = None,
               show_masks:bool = False, quiet:bool = True):

    import pdb; pdb.set_trace()

    #Print program header
    if not quiet:
        print(policygen_banner())

    policygen = PolicyGen(output = output,
                          min_length = min_length,
                          max_length = max_length,
                          min_digit = min_digit,
                          max_digit = max_digit,
                          min_upper = min_upper,
                          max_upper = max_upper,
                          min_lower = min_lower,
                          max_lower = max_lower,
                          min_special = min_special,
                          max_special = max_special,
                          show_masks = show_masks)

    print("[*] Generating masks.")
    policygen.generate_masks()
    if output:
        print("[*] Saving generated masks to [%s]" % output)


if __name__=="__main__":
    min_length = 4
    max_length = 6
    min_lower = 2
    min_upper = 1
    min_digits = 1

    output = "poli.hcmasks"

    policygen(output=output,
              min_length=min_length,
              max_length=max_length,
              min_lower=min_lower,
              min_upper=min_upper,
              min_digit=min_digits,
              show_masks=True)

#!/usr/bin/env python3
#
# policygen command line
#
# Maintainer: glozanoa <glozanoa@uni.pe>

import argparse
from fineprint.status import print_failure

from ..policygen import PolicyGen


def policygen_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", default=None, required=True,
                        help="Output File")
    parser.add_argument("--minlength", type=int, default=None,
                        help="Minimum password length")
    parser.add_argument("--maxlength", type=int, default=None,
                        help="Maximum password length")
    parser.add_argument("--mindigit", type=int, default=None,
                        help="Minimum number of digits")
    parser.add_argument("--maxdigit", type=int, default=None,
                        help="Maximum number of digits")
    parser.add_argument("--minupper", type=int, default=None,
                        help="Minimum number of upper alpha characters")
    parser.add_argument("--maxupper", type=int, default=None,
                        help="Maximum number of upper alpha characters")
    parser.add_argument("--minlower", type=int, default=None,
                        help="Minimum number of lower alpha characters")
    parser.add_argument("--maxlower", type=int, default=None,
                        help="Maximum number of lower alpha characters")
    parser.add_argument("--minspecial", type=int, default=None,
                        help="Minimum number of special characters")
    parser.add_argument("--maxspecial", type=int, default=None,
                        help="Maximum number of special characters")
    parser.add_argument("-s", "--showmasks", action='store_true',
                        help="Show generated masks")
    parser.add_argument("-q", "--quiet", action='store_true',
                        help="Run quietly")

    return parser



#debugged - date: Mar 7 2021
@staticmethod
def policygen( *,
               output: str = None,
               min_length:int = None, max_length:int = None, min_digit:int = None, max_digit: int = None,
               min_upper:int = None, max_upper:int = None, min_lower:int = None, max_lower:int = None,
               min_special:int = None, max_special:int = None,
               show_masks:bool = False, quiet:bool = True):

    #import pdb; pdb.set_trace()
    #Print program header
    if not quiet:
        print(PolicyGen.banner)

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

    if not quiet:
        print("[*] Generating masks.")
    policygen.generate_masks()
    if output and not quiet:
        print("[*] Saving generated masks to [%s]" % output)


def main():

    parser = policygen_parser()
    args = parser.parse_args()

    policygen(output = args.output,
              min_length = args.minlength,
              max_length = args.maxlength,
              min_digit = args.mindigits,
              max_digit = args.maxdigits,
              min_upper = args.minupper,
              max_upper = args.maxupper,
              min_lower = args.minlower,
              max_lower = args.maxlower,
              min_special = args.minspecial,
              max_special = args.maxspecial,
              show_masks = args.showmasks,
              quiet = args.quiet)

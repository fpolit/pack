#!/usr/bin/python3
# PolicyGen - Analyze and Generate password masks according to a password policy
#
# This tool is part of PACK (Password Analysis and Cracking Kit)
#
# VERSION 0.0.2
#
# Copyright (C) 2013 Peter Kacherginsky
# All rights reserved.
#
# Please see the attached LICENSE file for additional licensing information.

import sys, string, random
import datetime
from optparse import OptionParser, OptionGroup
import itertools


class PolicyGen:
    def __init__(self, *,
                 output: str = None,
                 min_length:int = 8,
                 max_length:int = 8,
                 min_digit:int = None,
                 max_digit: int = None,
                 min_upper:int = None,
                 max_upper:int = None,
                 min_lower:int = None,
                 max_lower:int = None,
                 min_special:int = None,
                 max_special:int = None,
                 show_masks:bool = False):
        self.output_file = output

        self.minlength  = min_length
        self.maxlength  = max_length
        self.mindigit   = min_digit   or 0
        self.minlower   = min_lower   or 0
        self.minupper   = min_upper   or 0
        self.minspecial = min_special or 0

        self.min_charsets = sum([self.mindigit, self.minlower, self.minupper, self.minspecial])
        max_char = self.maxlength - self.min_charsets

        self.maxdigit   = max_digit   or max_char + self.mindigit   if self.mindigit   > 0 else self.maxlength
        self.maxlower   = max_lower   or max_char + self.minlower   if self.minlower   > 0 else self.maxlength
        self.maxupper   = max_upper   or max_char + self.minupper   if self.minupper   > 0 else self.maxlength
        self.maxspecial = max_special or max_char + self.minspecial if self.minspecial > 0 else self.maxlength

        # PPS (Passwords per Second) Cracking Speed
        self.pps = 1000000000
        self.showmasks = show_masks

    def getcomplexity(self, mask):
        """ Return mask complexity. """
        count = 1
        for char in mask[1:].split("?"):
            if char == "l":   count *= 26
            elif char == "u": count *= 26
            elif char == "d": count *= 10
            elif char == "s": count *= 33
            elif char == "a": count *= 95
            else: print("[!] Error, unknown mask ?%s in a mask %s" % (char,mask))

        return count

    #debugged - date: Mar 7 2020
    def generate_masks(self):
        """ Generate all possible password masks matching the policy """

        #import pdb; pdb.set_trace()

        print("[*] Using {:,d} keys/sec for calculations.".format(self.pps))

        #Print current password policy
        print("[*] Password policy:")
        print("    Pass Lengths: min:%d max:%d" % (self.minlength, self.maxlength))
        print("    Min strength: l:%s u:%s d:%s s:%s" % \
              (self.minlower, self.minupper, self.mindigit, self.minspecial))
        print("    Max strength: l:%s u:%s d:%s s:%s" % \
              (self.maxlower, self.maxupper, self.maxdigit, self.maxspecial))

        output = None

        try:
            total_count = 0
            sample_count = 0

            # NOTE: It is better to collect total complexity
            #       not to lose precision when dividing by pps
            total_complexity = 0
            sample_complexity = 0

            if self.output_file:
                output = open(self.output_file, 'w')

            # TODO: Randomize or even statistically arrange matching masks
            for length in range(self.minlength, self.maxlength+1):
                #print("\n[*] Generating %d character password masks." % length)
                total_length_count = 0
                sample_length_count = 0


                total_length_complexity = 0
                sample_length_complexity = 0

                for masklist in itertools.product(['?d','?l','?u','?s'], repeat=length):

                    mask = ''.join(masklist)

                    lowercount = 0
                    uppercount = 0
                    digitcount = 0
                    specialcount = 0

                    mask_complexity = self.getcomplexity(mask)
                    total_length_count += 1
                    total_length_complexity += mask_complexity

                    # Count charachter types in a mask
                    for char in mask[1:].split("?"):
                        if char == "l": lowercount += 1
                        elif char == "u": uppercount += 1
                        elif char == "d": digitcount += 1
                        elif char == "s": specialcount += 1

                    # Filter according to password policy
                    if ((self.minlower   == None or lowercount   >= self.minlower) and \
                        (self.maxlower   == None or lowercount   <= self.maxlower) and \
                        (self.minupper   == None or uppercount   >= self.minupper) and \
                        (self.maxupper   == None or uppercount   <= self.maxupper) and \
                        (self.mindigit   == None or digitcount   >= self.mindigit) and \
                        (self.maxdigit   == None or digitcount   <= self.maxdigit) and \
                        (self.minspecial == None or specialcount >= self.minspecial) and \
                        (self.maxspecial == None or specialcount <= self.maxspecial)):

                        sample_length_count += 1
                        sample_length_complexity += mask_complexity

                        if self.showmasks:
                            mask_time = mask_complexity/self.pps
                            time_human = ">1 year" if mask_time > 60*60*24*365 else str(datetime.timedelta(seconds=mask_time))
                            print("[{:>2}] {:<30} [l:{:>2} u:{:>2} d:{:>2} s:{:>2}] [{:>8}]  ".format(length, mask, lowercount,uppercount,digitcount,specialcount, time_human))

                        if output:
                            output.write("%s\n" % mask)

                    total_count += total_length_count
                    sample_count += sample_length_count

                    total_complexity += total_length_complexity
                    sample_complexity += sample_length_complexity


            total_time = total_complexity/self.pps
            total_time_human = ">1 year" if total_time > 60*60*24*365 else str(datetime.timedelta(seconds=total_time))
            print("[*] Total Masks:  %d Time: %s" % (total_count, total_time_human))

            sample_time = sample_complexity/self.pps
            sample_time_human = ">1 year" if sample_time > 60*60*24*365 else str(datetime.timedelta(seconds=sample_time))
            print("[*] Policy Masks: %d Time: %s" % (sample_count, sample_time_human))


        except Exception as error:
            print(error)

        finally:
            if output is not None:
                output.close()

#!/usr/bin/python3
# MaskGen - Generate Password Masks
#
# This tool is part of PACK (Password Analysis and Cracking Kit)
#
# VERSION 0.0.3
#
# Copyright (C) 2013 Peter Kacherginsky
# All rights reserved.
#
# Please see the attached LICENSE file for additional licensing information.

import sys
import csv
import datetime
from operator import itemgetter
from optparse import OptionParser, OptionGroup

class MaskGen:
    def __init__(self, *,
                 target_time:int = None,
                 output_file:str = None,
                 minlength:int = None,
                 maxlength:int = None,
                 mintime:int = None,
                 maxtime:int = None,
                 mincomplexity:int = None,
                 maxcomplexity:int = None,
                 minoccurrence:int = None,
                 maxoccurrence:int = None,
                 pps:int  = 1000000000,
                 showmasks:bool = False):

        # Masks collections with meta data
        self.masks = dict()

        self.target_time = target_time
        self.output_file = output_file

        self.minlength  = minlength
        self.maxlength  = maxlength
        self.mintime    = mintime
        self.maxtime    = maxtime
        self.mincomplexity = mincomplexity
        self.maxcomplexity = maxcomplexity
        self.minoccurrence = minoccurrence
        self.maxoccurrence = maxoccurrence

        self.customcharset1len = None
        self.customcharset2len = None
        self.customcharset3len = None
        self.customcharset4len = None

        # PPS (Passwords per Second) Cracking Speed
        self.pps = ps
        self.showmasks = showmasks

        # Counter for total masks coverage
        self.total_occurrence = 0

    def getcomplexity(self, mask):
        """ Return mask complexity. """
        count = 1
        for char in mask[1:].split("?"):
            if char == "l":   count *= 26
            elif char == "u": count *= 26
            elif char == "d": count *= 10
            elif char == "s": count *= 33
            elif char == "a": count *= 95
            elif char == "b": count *= 256
            elif char == "h": count *= 16
            elif char == "H": count *= 16
            elif char == "1" and self.customcharset1len: count *= self.customcharset1len
            elif char == "2" and self.customcharset2len: count *= self.customcharset2len
            elif char == "3" and self.customcharset3len: count *= self.customcharset3len
            elif char == "4" and self.customcharset4len: count *= self.customcharset4len
            else: print("[!] Error, unknown mask ?%s in a mask %s" % (char,mask))

        return count

    def loadmasks(self, filename):
        """ Load masks and apply filters. """
        maskReader = csv.reader(open(filename,'r'), delimiter=',', quotechar='"')

        for (mask,occurrence) in maskReader:

            if mask == "": continue

            mask_occurrence = int(occurrence)
            mask_length = len(mask)/2
            mask_complexity = self.getcomplexity(mask)
            mask_time = mask_complexity/self.pps

            self.total_occurrence += mask_occurrence

            # Apply filters based on occurrence, length, complexity and time
            if (self.minoccurrence == None or mask_occurrence >= self.minoccurrence) and \
               (self.maxoccurrence == None or mask_occurrence <= self.maxoccurrence) and \
               (self.mincomplexity == None or mask_complexity >= self.mincomplexity) and \
               (self.maxcomplexity == None or mask_complexity <= self.maxcomplexity) and \
               (self.mintime == None or mask_time >= self.mintime) and \
               (self.maxtime == None or mask_time <= self.maxtime) and \
               (self.maxlength == None or mask_length <= self.maxlength) and \
               (self.minlength == None or mask_length >= self.minlength):

                self.masks[mask] = dict()
                self.masks[mask]['length'] = mask_length
                self.masks[mask]['occurrence'] = mask_occurrence
                self.masks[mask]['complexity'] = 1 - mask_complexity
                self.masks[mask]['time'] = mask_time
                self.masks[mask]['optindex'] = 1 - mask_complexity/mask_occurrence

    def generate_masks(self,sorting_mode):
        """ Generate optimal password masks sorted by occurrence, complexity or optindex """

        output = None
        try:
            sample_count = 0
            sample_time = 0
            sample_occurrence = 0

            # TODO Group by time here 1 minutes, 1 hour, 1 day, 1 month, 1 year....
            #      Group by length   1,2,3,4,5,6,7,8,9,10....
            #      Group by occurrence 10%, 20%, 30%, 40%, 50%....

            if self.showmasks: print("[L:] Mask:                          [ Occ:  ] [ Time:  ]")

            if self.output_file:
                output = open(self.output_file, 'w')

            for mask in sorted(self.masks.keys(), key=lambda mask: self.masks[mask][sorting_mode], reverse=True):

                if self.showmasks:
                    time_human = ">1 year" if self.masks[mask]['time'] > 60*60*24*365 else str(datetime.timedelta(seconds=self.masks[mask]['time']))
                    print("[{:>2}] {:<30} [{:<7}] [{:>8}]  ".format(self.masks[mask]['length'], mask, self.masks[mask]['occurrence'], time_human))

                if output:
                    output.write("%s\n" % mask)

                sample_occurrence += self.masks[mask]['occurrence']
                sample_time += self.masks[mask]['time']
                sample_count += 1

                if self.target_time and sample_time > self.target_time:
                    print("[!] Target time exceeded.")
                    break

            print("[*] Finished generating masks:")
            print("    Masks generated: %s" % sample_count)
            print("    Masks coverage:  %d%% (%d/%d)" % (sample_occurrence*100/self.total_occurrence,sample_occurrence,self.total_occurrence))
            time_human = ">1 year" if sample_time > 60*60*24*365 else str(datetime.timedelta(seconds=sample_time))
            print("    Masks runtime:   %s" % time_human)


        except Exception as error:
            print(error)

        finally:
            if output is not None:
                output.close()

    def getmaskscoverage(self, checkmasks):
        output = None
        try:
            sample_count = 0
            sample_occurrence = 0

            total_complexity = 0

            if self.output_file:
                output = open(self.output_file, 'w')

            if self.showmasks: print("[L:] Mask:                          [ Occ:  ] [ Time:  ]")
            for mask in checkmasks:
                mask = mask.strip()
                mask_complexity = self.getcomplexity(mask)

                total_complexity += mask_complexity

                if mask in self.masks:

                    if self.showmasks:
                        time_human = ">1 year" if self.masks[mask]['time'] > 60*60*24*365 else str(datetime.timedelta(seconds=self.masks[mask]['time']))
                        print("[{:>2}] {:<30} [{:<7}] [{:>8}]  ".format(self.masks[mask]['length'], mask, self.masks[mask]['occurrence'], time_human))

                    if output:
                        output.write("%s\n" % mask)

                    sample_occurrence += self.masks[mask]['occurrence']
                    sample_count += 1

                if self.target_time and total_complexity/self.pps > self.target_time:
                    print("[!] Target time exceeded.")
                    break

            # TODO: Something wrong here, complexity and time doesn't match with estimated from policygen
            total_time = total_complexity/self.pps
            time_human = ">1 year" if total_time > 60*60*24*365 else str(datetime.timedelta(seconds=total_time))
            print("[*] Finished matching masks:")
            print("    Masks matched: %s" % sample_count)
            print("    Masks coverage:  %d%% (%d/%d)" % (sample_occurrence*100/self.total_occurrence,sample_occurrence,self.total_occurrence))
            print("    Masks runtime:   %s" % time_human)


        except Exception as error:
            print(error)

        finally:
            if output is not None:
                output.close()

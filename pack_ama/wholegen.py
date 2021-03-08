#!/usr/bin/env python3
#
# wholegen - Perform a full analysis (statsgen and maskgen) to a wordlist and generate masks
#
# implemetation - date: Mar 7 2021
#
# Maintainer: glozanoa <glozanoa@uni.pe>

from typing import List

# statsgen
import sys
import re, operator, string
#from optparse import OptionParser, OptionGroup
import time

## maskgem
#import sys
#import csv
import datetime
from operator import itemgetter
#from optparse import OptionParser, OptionGroup
from math import floor



class WholeGen:
    """
    Perform a full analysis (statsgen and maskgen) to a wordlist and generate masks
    """

    def __init__(self, *,
                 #files
                 wordlist: str, output: str,
                 #filters
                 charsets: List[str] = None,
                 minlength: int      = None, maxlength: int    = None,
                 mindigit:int        = None, maxdigit:int      = None,
                 minupper:int        = None, maxupper:int      = None,
                 minlower:int        = None, maxlower:int      = None,
                 minspecial:int      = None, maxspecial:int    = None,
                 mincomplexity:int   = None, maxcomplexity:int = None,
                 minoccurrence:int   = None, maxoccurrence:int = None,
                 mintime:int         = None, maxtime:int       = None,
                 target_time:int     = None,
                 hiderare: int       = 0,

                 #print
                 showmasks:bool = False, quiet: bool = False):



        # files
        self.wordlist = wordlist
        self.output = output


        # Filters
        self.charsets      = charsets
        self.minlength     = minlength
        self.maxlength     = maxlength
        self.mindigit      = mindigit
        self.minupper      = minupper
        self.minlower      = minlower
        self.minspecial    = minspecial
        self.maxdigit      = maxdigit
        self.maxupper      = maxupper
        self.maxlower      = maxlower
        self.maxspecial    = maxspecial
        self.mincomplexity = mincomplexity
        self.maxcomplexity = maxcomplexity
        self.minoccurrence = minoccurrence
        self.maxoccurrence = maxoccurrence
        self.mintime       = mintime
        self.maxtime       = maxtime
        self.target_time   = target_time
        self.hiderare      = hiderare

        # print
        self.showmasks = showmasks
        self.quiet = quiet
        self.debug = False


        # Stats dictionaries
        self.stats_length = dict()
        self.stats_simplemasks = dict()
        self.stats_advancedmasks = dict()
        self.stats_charactersets = dict()

        # stats about password policy
        self.global_mindigit   = None
        self.global_minupper   = None
        self.global_minlower   = None
        self.global_minspecial = None

        self.global_maxdigit   = None
        self.global_maxupper   = None
        self.global_maxlower   = None
        self.global_maxspecial = None


        self.filter_counter = 0
        self.total_counter = 0


        # Masks collections with meta data
        self.masks = dict()

        self.customcharset1len = None
        self.customcharset2len = None
        self.customcharset3len = None
        self.customcharset4len = None

        # PPS (Passwords per Second) Cracking Speed
        self.pps = 1000000000

        # Counter for total masks coverage
        self.total_occurrence = 0


    def analyze_password(self, password):

        # Password length
        pass_length = len(password)

        # Character-set and policy counters
        digit = 0
        lower = 0
        upper = 0
        special = 0

        #simplemask = list()
        advancedmask_string = ""

        # Detect simple and advanced masks
        for letter in password:
            if letter in string.digits:
                digit += 1
                advancedmask_string += "?d"
                #if not simplemask or not simplemask[-1] == 'digit': simplemask.append('digit')

            elif letter in string.ascii_lowercase:
                lower += 1
                advancedmask_string += "?l"
                #if not simplemask or not simplemask[-1] == 'string': simplemask.append('string')


            elif letter in string.ascii_uppercase:
                upper += 1
                advancedmask_string += "?u"
                #if not simplemask or not simplemask[-1] == 'string': simplemask.append('string')

            else:
                special += 1
                advancedmask_string += "?s"
                #if not simplemask or not simplemask[-1] == 'special': simplemask.append('special')


        # String representation of masks
        #simplemask_string = ''.join(simplemask) if len(simplemask) <= 3 else 'othermask'

        # Policy
        policy = (digit,lower,upper,special)

        # Determine character-set
        if   digit and not lower and not upper and not special: charset = 'numeric'
        elif not digit and lower and not upper and not special: charset = 'loweralpha'
        elif not digit and not lower and upper and not special: charset = 'upperalpha'
        elif not digit and not lower and not upper and special: charset = 'special'

        elif not digit and lower and upper and not special:     charset = 'mixedalpha'
        elif digit and lower and not upper and not special:     charset = 'loweralphanum'
        elif digit and not lower and upper and not special:     charset = 'upperalphanum'
        elif not digit and lower and not upper and special:     charset = 'loweralphaspecial'
        elif not digit and not lower and upper and special:     charset = 'upperalphaspecial'
        elif digit and not lower and not upper and special:     charset = 'specialnum'

        elif not digit and lower and upper and special:         charset = 'mixedalphaspecial'
        elif digit and not lower and upper and special:         charset = 'upperalphaspecialnum'
        elif digit and lower and not upper and special:         charset = 'loweralphaspecialnum'
        elif digit and lower and upper and not special:         charset = 'mixedalphanum'
        else:                                                   charset = 'all'

        return (pass_length, charset, advancedmask_string, policy)


    # statsgen
    def generate_stats(self):
        """ Generate password statistics. """

        import pdb; pdb.set_trace()

        with open(self.wordlist_file, 'r') as f:

            for password in f:
                password = password.rstrip('\r\n')

                if len(password) == 0: continue

                self.total_counter += 1

                (pass_length, characterset, advancedmask, policy) = self.analyze_password(password)
                (digit,lower,upper,special) = policy

                if (self.charsets == None    or characterset in self.charsets) and \
                   (self.maxlength == None   or pass_length <= self.maxlength) and \
                   (self.minlength == None   or pass_length >= self.minlength) and \
                   (self.mindigit == None or digit >= self.mindigit) and \
                   (self.maxdigit == None or digit <= self.maxdigit) and \
                   (self.minupper == None or upper >= self.minupper) and \
                   (self.maxupper == None or upper <= self.maxupper) and \
                   (self.minlower == None or lower >= self.minlower) and \
                   (self.maxlower == None or lower <= self.maxlower) and \
                   (self.minspecial == None or special >= self.minspecial) and \
                   (self.maxspecial == None or special <= self.maxspecial):

                    self.filter_counter += 1

                    if self.global_mindigit == None or digit < self.global_mindigit:
                        self.global_mindigit = digit

                    if self.global_maxdigit == None or digit > self.global_maxdigit:
                        self.global_maxdigit = digit

                    if self.global_minupper == None or upper < self.global_minupper:
                        self.global_minupper = upper

                    if self.global_maxupper == None or upper > self.global_maxupper:
                        self.global_maxupper = upper

                    if self.global_minlower == None or lower < self.global_minlower:
                        self.global_minlower = lower

                    if self.global_maxlower == None or lower > self.global_maxlower:
                        self.global_maxlower = lower

                    if self.global_minspecial == None or special < self.global_minspecial:
                        self.global_minspecial = special

                    if self.global_maxspecial == None or special > self.global_maxspecial:
                        self.global_maxspecial = special

                    if pass_length in self.stats_length:
                        self.stats_length[pass_length] += 1
                    else:
                        self.stats_length[pass_length] = 1

                    if characterset in self.stats_charactersets:
                        self.stats_charactersets[characterset] += 1
                    else:
                        self.stats_charactersets[characterset] = 1

                    # if simplemask in self.stats_simplemasks:
                    #     self.stats_simplemasks[simplemask] += 1
                    # else:
                    #     self.stats_simplemasks[simplemask] = 1

                    if advancedmask in self.stats_advancedmasks:
                        self.stats_advancedmasks[advancedmask] += 1
                    else:
                        self.stats_advancedmasks[advancedmask] = 1


    #maskgen
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

    #maskgen
    def loadmasks(self):
        """ Load masks and apply filters. """
        import pdb; pdb.set_trace()

        maskReader = self.stats_advancedmasks.items()

        for (mask,occurrence) in maskReader:

            if mask == "": continue

            mask_occurrence = int(occurrence)
            mask_length = floor(len(mask)/2)
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
               (mask_occurrence*100/self.filter_counter > self.hiderare):

                self.masks[mask] = dict()
                self.masks[mask]['length'] = mask_length
                self.masks[mask]['occurrence'] = mask_occurrence
                self.masks[mask]['complexity'] = 1 - mask_complexity
                self.masks[mask]['time'] = mask_time
                self.masks[mask]['optindex'] = 1 - mask_complexity/mask_occurrence

    #maskgen
    #debugged - date: Mar 7 2021
    def generate_masks(self,sorting_mode):
        """ Generate optimal password masks sorted by occurrence, complexity or optindex """

        import pdb; pdb.set_trace()
        self.loadmasks()
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
            #print("    Masks coverage:  %d%% (%d/%d)" % (sample_occurrence*100/self.total_occurrence,sample_occurrence,self.total_occurrence))
            time_human = ">1 year" if sample_time > 60*60*24*365 else str(datetime.timedelta(seconds=sample_time))
            print("    Masks runtime:   %s" % time_human)


        except Exception as error:
            print(error)

        finally:
            if output is not None:
                output.close()

    def full_analysis(self):
        self.generate_stats()
        self.generate_masks()


if __name__=="__main__":
    wordlist = "wl/john.txt"
    output = "john.hcmasks"
    whole = WholeGen(wordlist=wordlist,
                     output=output)

    whole.full_analysis()

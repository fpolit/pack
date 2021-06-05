#!/usr/bin/env python3
#
# statsgen command line
#
# Maintainer: glozanoa <glozanoa@uni.pe>



    @staticmethod
    def wholegen(*,
                 wordlist: str, output: str,
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
                 showmasks:bool = False, quiet: bool = False,
                 sorting = "optindex"):

        #import pdb; pdb.set_trace()

        try:
            permission = [os.R_OK]
            Path.access(permission, wordlist)


            print(f"[*] Analyzing passwords in {wordlist}")

            whole = WholeGen(
                wordlist = wordlist,
                output = output,
                charsets = charsets,
                minlength = minlength,
                maxlength = maxlength,
                mindigit = mindigit,
                maxdigit = maxdigit,
                minupper = minupper,
                maxupper = maxupper,
                minlower = minlower,
                maxlower = maxlower,
                minspecial = minspecial,
                maxspecial = maxspecial,
                mincomplexity = mincomplexity,
                maxcomplexity = maxcomplexity,
                minoccurrence = minoccurrence,
                maxoccurrence = maxoccurrence,
                mintime = mintime,
                maxtime = maxtime,
                target_time = target_time,
                hiderare = hiderare,
                showmasks = showmasks,
                quiet = quiet)

            whole.full_analysis(sorting)


        except Exception as error:
            print_failure(error)




def main():
    wordlist = "wl/john.txt"
    output = "john.hcmasks"
    whole = WholeGen(wordlist=wordlist,
                     output=output)

    whole.full_analysis()

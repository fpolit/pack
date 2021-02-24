#!/usr/bin/env python3
#
# pack banner
#
# date: Feb 23 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# import pack version
from version import getPackversion

def getPackBanner():
    VERSION = getPackversion()
    banner  = "                       _ \n"
    banner += "     StatsGen %s   | |\n"  % VERSION
    banner += "      _ __   __ _  ___| | _\n"
    banner += "     | '_ \ / _` |/ __| |/ /\n"
    banner += "     | |_) | (_| | (__|   < \n"
    banner += "     | .__/ \__,_|\___|_|\_\\\n"
    banner += "     | |                    \n"
    banner += "     |_| iphelix@thesprawl.org\n"
    banner += "\n"

    return banner

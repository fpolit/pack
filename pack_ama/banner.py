#!/usr/bin/env python3
#
# pack banner
#
# date: Feb 23 2021
# Maintainer: glozanoa <glozanoa@uni.pe>

# import pack version
from .version import pack_version

def statsgen_banner():
    VERSION = pack_version()
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


def maskgen_banner():
    VERSION = pack_version()
    banner  = "                       _ \n"
    banner += "     MaskGen %s    | |\n" % VERSION
    banner += "      _ __   __ _  ___| | _\n"
    banner += "     | '_ \ / _` |/ __| |/ /\n"
    banner += "     | |_) | (_| | (__|   < \n"
    banner += "     | .__/ \__,_|\___|_|\_\\\n"
    banner += "     | |                    \n"
    banner += "     |_| iphelix@thesprawl.org\n"
    banner += "\n"

    return banner


def policygen_banner():
    VERSION = pack_version()
    banner  = "                       _ \n"
    banner += "     PolicyGen %s  | |\n"  % VERSION
    banner += "      _ __   __ _  ___| | _\n"
    banner += "     | '_ \ / _` |/ __| |/ /\n"
    banner += "     | |_) | (_| | (__|   < \n"
    banner += "     | .__/ \__,_|\___|_|\_\\\n"
    banner += "     | |                    \n"
    banner += "     |_| iphelix@thesprawl.org\n"
    banner += "\n"

    return banner

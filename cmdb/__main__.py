#!/usr/bin/env python
"""
Net|CMDB is a flexible asset management tool and
open-source configurable management database

You should have received a copy of the MIT License along with Net|CMDB.
If not, see <https://github.com/NETHINKS/NetCMDB/blob/master/LICENSE>.
"""
from cmdb import __version__, __title__, __DEBUG__
from optparse import OptionParser


def build_argparser():
    _parser = OptionParser(
        usage="usage: {} [options]".format(__title__),
        version=" {}".format(__version__)
    )
    _parser.add_option("-d", "--debug", action="callback", callback=dev,
                       help="enable debug mode: DO NOT USE ON PRODUCTIVE SYSTEMS")
    (options, args) = _parser.parse_args()
    return _parser


def dev(*args):
    """
    Quick test function
    """
    global __DEBUG__
    __DEBUG__ = True


def main(args):
    pass


if __name__ == "__main__":
    parser = build_argparser()

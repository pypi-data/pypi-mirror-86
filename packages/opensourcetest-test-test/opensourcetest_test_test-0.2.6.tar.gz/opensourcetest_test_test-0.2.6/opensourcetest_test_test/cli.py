#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : opensourcetest_test_test
@Time    : 2020/10/13 14:01
@Auth    : chineseluo
@Email   : 848257135@qq.com
@File    : cli.py
@IDE     : PyCharm
------------------------------------
"""
import os
from loguru import logger
import sys
import argparse
from .scaffold import create_scaffold
from opensourcetest_test_test import __version__, __description__


def init_scaffold_parser(subparsers):
    sub_scaffold_parser = subparsers.add_parser(
        "startproject", help="Create a new project with template structure."
    )
    sub_scaffold_parser.add_argument(
        "project_name", type=str, nargs="?", help="Specify new project name."
    )
    return sub_scaffold_parser


def init_docs_scaffold_parser(subparsers):
    sub_docs_scaffold_parser = subparsers.add_parser(
        "onlinedocs", help="Welcome to the online documentation:http://docs.opensourcetest.cn"
    )
    return sub_docs_scaffold_parser

def main():
    # Generate subcommand object
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-v", "-V", "--version", "--Version", dest="version", action="store_true", help="show version")
    subparsers = parser.add_subparsers(help="OpenSourceTest sub-command help")
    sub_scaffold_parser = init_scaffold_parser(subparsers)
    sub_docs_scaffold_parser = init_docs_scaffold_parser(subparsers)
    ost_argv = sys.argv
    print(ost_argv)
    if len(ost_argv) == 1:
        parser.print_help()
        sys.exit()
    elif len(ost_argv) == 2:
        if ost_argv[1] in ["-V", "-v", "--Version", "--version"]:
            print(f"""
             +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +++ +-+ +++ +-+ +++ +-+ +++ +-+
             | O | | p | | e | | n | | S | | o | | u | | r | | c | | e | | T | | e | | s | | t |
             +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +++ +-+ +++ +-+ +++ +-+ +++ +-+
            """)
            logger.info(f"The OpenSourceTest version is {__version__}")
        elif ost_argv[1] in ["-h", "-H", "--help", "--Help"]:
            parser.print_help()
        elif ost_argv[1] == "startproject":
            sub_scaffold_parser.print_help()
        elif ost_argv[1] == "onlinedocs":
            logger.info("Welcome to the online documentation:http://docs.opensourcetest.cn")
        else:
            print("Please use nm - h to view help information")
        sys.exit(0)
    elif len(sys.argv) == 3 and sys.argv[1] == "startproject" and sys.argv[2] in ["-h", "-H", "--help", "--Help"]:
        logger.info("Please follow OST startproject with the project file name!")
        sys.exit(0)
    elif len(sys.argv) == 3 and sys.argv[1] == "startproject":
        create_scaffold(sys.argv[2])
        sys.exit(0)


if __name__ == "__main__":
    print(f"""
                +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +++ +-+ +++ +-+ +++ +-+ +++ +-+
                | O | | p | | e | | n | | S | | o | | u | | r | | c | | e | | T | | e | | s | | t |
                +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +-+ +++ +-+ +++ +-+ +++ +-+ +++ +-+
               """)
    logger.info(f"The OpenSourceTest version is {__version__}")

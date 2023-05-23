#!/usr/bin/env python
"""Entrypoint of the module."""

import sys
import pathlib
import argparse
import configparser
from typing import Optional, List


def parse_arguments(args:List[str]) -> argparse.Namespace:
    """Parse command-line arguments and return the attributes.

    Parameters
    ----------
    args : List
        Arguments

    Returns
    -------
    argparse.Namespace
        Simple object holding the attributes as fields.
    """
    parser = argparse.ArgumentParser(
        description='A random assortment of Quantitative Finance algorithms that are implemented to be differentiable.'
    )
    parser.add_argument(
        '-o',
        '--output-path',
        type=str,
        default='dfin-output',
        help='Directory to store outputs. Default: "dfin-output".'
    )
    parser.add_argument(
        '-l',
        '--log-path',
        type=str,
        default='dfin-log',
        help='Directory to store logs. Default: "dfin-log".'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true'
    )
    parser.add_argument(
        '-s',
        '--start',
        action='store_true'
    )
    return parser.parse_args(args)


def main_cli(args:Optional[List[str]]=None):
    """Entry point of the module."""

    if args is None:
        args = parse_arguments(sys.argv[1:])
    else:
        args = parse_arguments(args)

    if args.verbose:
        print('Input arguments:')
        print(args)

    if args.verbose:
        print('==============================')
        print('=====        dFin        =====')
        print('==============================')
        print('                              ')

    if args.start:
        import streamlit.web.bootstrap
        app_path = pathlib.Path(__file__).parent / 'app' / '💰_dFin.py'
        print(app_path.as_posix())
        st_cli = ''
        st_args = [
        ]
        st_flags = {
        }
        streamlit.web.bootstrap.run(app_path.as_posix(), st_cli, st_args, st_flags)

    if args.verbose:
        print('                              ')
        print('==============================')
        print('=====   End of program   =====')
        print('==============================')



if __name__ == "__main__":

    main_cli(['-v'])

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**slice_reStructuredText.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Slices given reStructuredText file.

**Others:**

"""

from __future__ import unicode_literals

import argparse
import os
import re
import sys

if sys.version_info[:2] <= (2, 6):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

import foundations.decorators
import foundations.verbose
from foundations.io import File

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "OUTPUT_FILES_EXTENSION",
           "SLICE_ATTRIBUTE_INDENT",
           "CONTENT_DELETION",
           "STATEMENT_SUBSTITUTE",
           "slice_reStructuredText",
           "get_command_line_arguments",
           "main"]

LOGGER = foundations.verbose.install_logger()

OUTPUT_FILES_EXTENSION = "rst"
SLICE_ATTRIBUTE_INDENT = 2
CONTENT_DELETION = ()
STATEMENT_SUBSTITUTE = {"resources/": "../",
                         "     \|": "            |"}

foundations.verbose.get_logging_console_handler()
foundations.verbose.set_verbosity_level(3)

def slice_reStructuredText(input, output):
    """
    Slices given reStructuredText file.

    :param input: ReStructuredText file to slice.
    :type input: unicode
    :param output: Directory to output sliced reStructuredText files.
    :type output: unicode
    :return: Definition success.
    :rtype: bool
    """

    LOGGER.info("{0} | Slicing '{1}' file!".format(slice_reStructuredText.__name__, input))
    file = File(input)
    file.cache()

    slices = OrderedDict()
    for i, line in enumerate(file.content):
        search = re.search(r"^\.\. \.(\w+)", line)
        if search:
            slices[search.groups()[0]] = i + SLICE_ATTRIBUTE_INDENT

    index = 0
    for slice, slice_start in slices.iteritems():
        slice_file = File(os.path.join(output, "{0}.{1}".format(slice, OUTPUT_FILES_EXTENSION)))
        LOGGER.info("{0} | Outputing '{1}' file!".format(slice_reStructuredText.__name__, slice_file.path))
        slice_end = index < (len(slices.values()) - 1) and slices.values()[index + 1] - SLICE_ATTRIBUTE_INDENT or \
                   len(file.content)

        for i in range(slice_start, slice_end):
            skip_line = False
            for item in CONTENT_DELETION:
                if re.search(item, file.content[i]):
                    LOGGER.info("{0} | Skipping Line '{1}' with '{2}' content!".format(slice_reStructuredText.__name__,
                                                                                       i,
                                                                                       item))
                    skip_line = True
                    break

            if skip_line:
                continue

            line = file.content[i]
            for pattern, value in STATEMENT_SUBSTITUTE.iteritems():
                line = re.sub(pattern, value, line)

            search = re.search(r"-  `[\w ]+`_ \(([\w\.]+)\)", line)
            if search:
                LOGGER.info("{0} | Updating Line '{1}' link: '{2}'!".format(slice_reStructuredText.__name__,
                                                                            i,
                                                                            search.groups()[0]))
                line = "-  :ref:`{0}`\n".format(search.groups()[0])
            slice_file.content.append(line)

        slice_file.write()
        index += 1

    return True

def get_command_line_arguments():
    """
    Retrieves command line arguments.

    :return: Namespace.
    :rtype: Namespace
    """

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("-h",
                        "--help",
                        action="help",
                        help="'Displays this help message and exit.'")

    parser.add_argument("-i",
                        "--input",
                        type=unicode,
                        dest="input",
                        help="'ReStructuredText file to slice.'")

    parser.add_argument("-o",
                        "--output",
                        type=unicode,
                        dest="output",
                        help="'Directory to output sliced reStructuredText files.'")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

@foundations.decorators.system_exit
def main():
    """
    Starts the Application.

    :return: Definition success.
    :rtype: bool
    """

    args = get_command_line_arguments()
    return slice_reStructuredText(args.input,
                                 args.output)

if __name__ == "__main__":
    main()

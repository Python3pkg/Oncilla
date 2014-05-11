#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**build_toc_tree.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Builds Sphinx documentation Toc Tree file.

**Others:**

"""

from __future__ import unicode_literals

import argparse
import glob
import os
import re
import sys

if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict

import foundations.decorators
import foundations.strings
import foundations.verbose
from foundations.io import File

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		   "FILES_EXTENSION",
		   "TOCTREE_TEMPLATE_BEGIN",
		   "TOCTREE_TEMPLATE_END",
		   "build_toc_tree",
		   "get_command_line_arguments",
		   "main"]

LOGGER = foundations.verbose.install_logger()

FILES_EXTENSION = ".rst"

TOCTREE_TEMPLATE_BEGIN = ["Welcome to {0} |version|'s documentation!\n",
						  "{0}\n",
						  "\n",
						  "Contents:\n",
						  "\n",
						  ".. toctree::\n",
						  " :maxdepth: 2\n",
						  " :numbered:\n"]
TOCTREE_TEMPLATE_END = ["Search:\n",
						"==================\n",
						"\n",
						"* :ref:`genindex`\n",
						"* :ref:`modindex`\n",
						"* :ref:`search`\n", ]

foundations.verbose.get_logging_console_handler()
foundations.verbose.set_verbosity_level(3)

def build_toc_tree(title, input, output, content_directory):
	"""
	Builds Sphinx documentation table of content tree file.

	:param title: Package title.
	:type title: unicode
	:param input: Input file to convert.
	:type input: unicode
	:param output: Output file.
	:type output: unicode
	:param content_directory: Directory containing the content to be included in the table of content.
	:type content_directory: unicode
	:return: Definition success.
	:rtype: bool
	"""

	LOGGER.info("{0} | Building Sphinx documentation index '{1}' file!".format(build_toc_tree.__name__,
																			   output))
	file = File(input)
	file.cache()

	existing_files = [foundations.strings.get_splitext_basename(item)
					 for item in glob.glob("{0}/*{1}".format(content_directory, FILES_EXTENSION))]
	relative_directory = content_directory.replace("{0}/".format(os.path.dirname(output)), "")

	toc_tree = ["\n"]
	for line in file.content:
		search = re.search(r"`([a-zA-Z_ ]+)`_", line)
		if not search:
			continue

		item = search.groups()[0]
		code = "{0}{1}".format(item[0].lower(), item.replace(" ", "")[1:])
		if code in existing_files:
			link = "{0}/{1}".format(relative_directory, code)
			data = "{0}{1}{2} <{3}>\n".format(" ", " " * line.index("-"), item, link)
			LOGGER.info("{0} | Adding '{1}' entry to Toc Tree!".format(build_toc_tree.__name__,
																	   data.replace("\n", "")))
			toc_tree.append(data)
	toc_tree.append("\n")

	TOCTREE_TEMPLATE_BEGIN[0] = TOCTREE_TEMPLATE_BEGIN[0].format(title)
	TOCTREE_TEMPLATE_BEGIN[1] = TOCTREE_TEMPLATE_BEGIN[1].format("=" * len(TOCTREE_TEMPLATE_BEGIN[0]))
	content = TOCTREE_TEMPLATE_BEGIN
	content.extend(toc_tree)
	content.extend(TOCTREE_TEMPLATE_END)

	file = File(output)
	file.content = content
	file.write()

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

	parser.add_argument("-t",
						"--title",
						type=unicode,
						dest="title",
						help="'Package title.'")

	parser.add_argument("-i",
						"--input",
						type=unicode,
						dest="input",
						help="'Input file to convert.'")

	parser.add_argument("-o",
						"--output",
						type=unicode,
						dest="output",
						help="'Output file.'")

	parser.add_argument("-c",
						"--content_directory",
						type=unicode,
						dest="content_directory",
						help="'Content directory.'")

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
	return build_toc_tree(args.title,
						args.input,
						args.output,
						args.content_directory)

if __name__ == "__main__":
	main()

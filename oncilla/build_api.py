#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**build_api.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Builds Sphinx documentation Api files.

**Others:**

"""

from __future__ import unicode_literals

import argparse
import os
import shutil
import sys

if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict

import foundations.common
import foundations.decorators
import foundations.exceptions
import foundations.strings
import foundations.verbose
import foundations.walkers
from foundations.io import File

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libraries"))
import python.pyclbr as module_browser

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
		   "SANITIZER",
		   "import_sanitizer",
		   "build_api",
		   "get_command_line_arguments",
		   "main"]

LOGGER = foundations.verbose.install_logger()

FILES_EXTENSION = ".rst"

TOCTREE_TEMPLATE_BEGIN = ["Api\n",
						  "====\n",
						  "\n",
						  "Modules Summary:\n",
						  "\n",
						  ".. toctree::\n",
						  "   :maxdepth: 1\n",
						  "\n"]

TOCTREE_TEMPLATE_END = []

SANITIZER = os.path.join(os.path.dirname(__file__), "default_sanitizer.py")

foundations.verbose.get_logging_console_handler()
foundations.verbose.set_verbosity_level(3)

def import_sanitizer(sanitizer):
	"""
	Imports the sanitizer python module.

	:param sanitizer: Sanitizer python module file.
	:type sanitizer: unicode
	:return: Module.
	:rtype: object
	"""

	directory = os.path.dirname(sanitizer)
	not directory in sys.path and sys.path.append(directory)

	namespace = __import__(foundations.strings.get_splitext_basename(sanitizer))
	if hasattr(namespace, "bleach"):
		return namespace
	else:
		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' is not a valid sanitizer module file!".format(sanitizer))

def build_api(packages, input, output, sanitizer, excluded_modules=None):
	"""
	Builds the Sphinx documentation API.

	:param packages: Packages to include in the API.
	:type packages: list
	:param input: Input modules directory.
	:type input: unicode
	:param output: Output reStructuredText files directory.
	:type output: unicode
	:param sanitizer: Sanitizer python module.
	:type sanitizer: unicode
	:param excluded_modules: Excluded modules.
	:type excluded_modules: list
	:return: Definition success.
	:rtype: bool
	"""

	LOGGER.info("{0} | Building Sphinx documentation API!".format(build_api.__name__))

	sanitizer = import_sanitizer(sanitizer)

	if os.path.exists(input):
		shutil.rmtree(input)
		os.makedirs(input)

	excluded_modules = [] if excluded_modules is None else excluded_modules

	packages_modules = {"apiModules": [],
					   "testsModules": []}
	for package in packages:
		package = __import__(package)
		path = foundations.common.get_first_item(package.__path__)
		package_directory = os.path.dirname(path)

		for file in sorted(
				list(foundations.walkers.files_walker(package_directory, filters_in=("{0}.*\.ui$".format(path),)))):
			LOGGER.info("{0} | Ui file: '{1}'".format(build_api.__name__, file))
			target_directory = os.path.dirname(file).replace(package_directory, "")
			directory = "{0}{1}".format(input, target_directory)
			if not foundations.common.path_exists(directory):
				os.makedirs(directory)
			source = os.path.join(directory, os.path.basename(file))
			shutil.copyfile(file, source)

		modules = []
		for file in sorted(
				list(foundations.walkers.files_walker(package_directory, filters_in=("{0}.*\.py$".format(path),),
													 filters_out=excluded_modules))):
			LOGGER.info("{0} | Python file: '{1}'".format(build_api.__name__, file))
			module = "{0}.{1}".format((".".join(os.path.dirname(file).replace(package_directory, "").split("/"))),
									  foundations.strings.get_splitext_basename(file)).strip(".")
			LOGGER.info("{0} | Module name: '{1}'".format(build_api.__name__, module))
			directory = os.path.dirname(os.path.join(input, module.replace(".", "/")))
			if not foundations.common.path_exists(directory):
				os.makedirs(directory)
			source = os.path.join(directory, os.path.basename(file))
			shutil.copyfile(file, source)

			sanitizer.bleach(source)

			if "__init__.py" in file:
				continue

			rst_file_path = "{0}{1}".format(module, FILES_EXTENSION)
			LOGGER.info("{0} | Building API file: '{1}'".format(build_api.__name__, rst_file_path))
			rst_file = File(os.path.join(output, rst_file_path))
			header = ["_`{0}`\n".format(module),
					  "==={0}\n".format("=" * len(module)),
					  "\n",
					  ".. automodule:: {0}\n".format(module),
					  "\n"]
			rst_file.content.extend(header)

			functions = OrderedDict()
			classes = OrderedDict()
			module_attributes = OrderedDict()
			for member, object in module_browser._readmodule(module, [source, ]).iteritems():
				if object.__class__ == module_browser.Function:
					if not member.startswith("_"):
						functions[member] = [".. autofunction:: {0}\n".format(member)]
				elif object.__class__ == module_browser.Class:
					classes[member] = [".. autoclass:: {0}\n".format(member),
									   "	:show-inheritance:\n",
									   "	:members:\n"]
				elif object.__class__ == module_browser.Global:
					if not member.startswith("_"):
						module_attributes[member] = [".. attribute:: {0}.{1}\n".format(module, member)]

			module_attributes and rst_file.content.append("Module Attributes\n-----------------\n\n")
			for module_attribute in module_attributes.itervalues():
				rst_file.content.extend(module_attribute)
				rst_file.content.append("\n")

			functions and rst_file.content.append("Functions\n---------\n\n")
			for function in functions.itervalues():
				rst_file.content.extend(function)
				rst_file.content.append("\n")

			classes and rst_file.content.append("Classes\n-------\n\n")
			for class_ in classes.itervalues():
				rst_file.content.extend(class_)
				rst_file.content.append("\n")

			rst_file.write()
			modules.append(module)

		packages_modules["apiModules"].extend([module for module in modules if not "tests" in module])
		packages_modules["testsModules"].extend([module for module in modules if "tests" in module])

	api_file = File("{0}{1}".format(output, FILES_EXTENSION))
	api_file.content.extend(TOCTREE_TEMPLATE_BEGIN)
	for module in packages_modules["apiModules"]:
		api_file.content.append("   {0} <{1}>\n".format(module, "api/{0}".format(module)))
	for module in packages_modules["testsModules"]:
		api_file.content.append("   {0} <{1}>\n".format(module, "api/{0}".format(module)))
	api_file.content.extend(TOCTREE_TEMPLATE_END)
	api_file.write()

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

	parser.add_argument("-p",
						"--packages",
						dest="packages",
						nargs="+",
						help="'Packages to include in the API.'")

	parser.add_argument("-i",
						"--input",
						type=unicode,
						dest="input",
						help="'Input modules directory.'")

	parser.add_argument("-o",
						"--output",
						type=unicode,
						dest="output",
						help="'Output reStructuredText files directory.'")

	parser.add_argument("-s",
						"--sanitizer",
						type=unicode,
						dest="sanitizer",
						help="'Sanitizer python module'")

	parser.add_argument("-x",
						"--excluded_modules",
						dest="excluded_modules",
						nargs="*",
						help="'Excluded modules.'")

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
	args.sanitizer = args.sanitizer if foundations.common.path_exists(args.sanitizer) else SANITIZER
	args.excluded_modules = args.excluded_modules if all(args.excluded_modules) else []
	return build_api(args.packages,
					args.input,
					args.output,
					args.sanitizer,
					args.excluded_modules)

if __name__ == "__main__":
	main()

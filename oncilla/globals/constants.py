#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Oncilla** package default constants through the :class:`Constants` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import platform

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import oncilla

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["Constants"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Constants():
	"""
	Defines **Oncilla** package default constants.
	"""

	applicationName = "Oncilla"
	"""Package Application name: '**Oncilla**' ( String )"""
	majorVersion = "0"
	"""Package major version: '**0**' ( String )"""
	minorVersion = "1"
	"""Package minor version: '**1**' ( String )"""
	changeVersion = "0"
	"""Package change version: '**0**' ( String )"""
	releaseVersion = ".".join((majorVersion, minorVersion, changeVersion))
	"""Package release version: '**0.1.0**' ( String )"""

	logger = "Oncilla_Logger"
	"""Package logger name: '**Oncilla_Logger**' ( String )"""
	verbosityLevel = 3
	"""Default logging verbosity level: '**3**' ( Integer )"""
	verbosityLabels = ("Critical", "Error", "Warning", "Info", "Debug")
	"""Logging verbosity labels: ('**Critical**', '**Error**', '**Warning**', '**Info**', '**Debug**') ( Tuple )"""
	loggingDefaultFormatter = "Default"
	"""Default logging formatter name: '**Default**' ( String )"""
	loggingSeparators = "*" * 96
	"""Logging separators: '*' * 96 ( String )"""

	defaultCodec = oncilla.DEFAULT_CODEC
	"""Default codec: '**utf-8**' ( String )"""
	codecError = "ignore"
	"""Default codec error behavior: '**ignore**' ( String )"""
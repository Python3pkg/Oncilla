Oncilla
=======

Introduction
------------

**Oncilla** is the documentation building helper package of `Oncilla <http://github.com/KelSolaar/Oncilla>`_, `Manager <http://github.com/KelSolaar/Manager>`_, `Umbra <http://github.com/KelSolaar/Umbra>`_, `sIBL_GUI <http://github.com/KelSolaar/sIBL_GUI>`_ and `sIBL_Reporter <http://github.com/KelSolaar/sIBL_Reporter>`_.

Installation
------------

The following dependencies are needed:

-  **Python 2.6.7** or **Python 2.7.3**: http://www.python.org/
-  **PyQt**: http://www.riverbankcomputing.co.uk/
-  **Tidy** http://tidy.sourceforge.net/

To install **Oncilla** from the `Python Package Index <http://pypi.python.org/pypi/Oncilla>`_ you can issue this command in a shell::

	pip install Oncilla

or this alternative command::

	easy_install Oncilla

Alternatively, if you want to directly install from `Github <http://github.com/KelSolaar/Oncilla>`_ source repository::

	git clone git://github.com/KelSolaar/Oncilla.git
	cd Oncilla
	python setup.py install

Usage
-----

Once installed, you can launch **Oncilla** using this shell command::

      Oncilla

You will need to have the following environment variables defined:

-  **ONCILLA_PROJECT_DIRECTORY**: Defines the project directory you want to build the manual and **Sphinx** documentation.
-  **ONCILLA_PROJECT_NAME**: Defines the name you want to use across the manual and **Sphinx** documentation files.
-  **ONCILLA_PROJECT_PACKAGES**: Defines the packages you want to build the **Sphinx** documentation.
-  **ONCILLA_PROJECT_SANITIZER**: Defines the optional **Sphinx** documentation sanitizing **Python** module.
-  **ONCILLA_PROJECT_EXCLUDED_MODULES**: Defines the optional excluded **Python** modules from **Sphinx** documentation.

Example:

	export ONCILLA_PROJECT_DIRECTORY="/Users/kelsolaar/Documents/Development/sIBL_GUI"
	export ONCILLA_PROJECT_NAME="sIBL_GUI"
	export ONCILLA_PROJECT_PACKAGES="oncilla foundations manager umbra sibl_gui"
	export ONCILLA_PROJECT_SANITIZER="/Users/kelsolaar/Documents/Development/sIBL_GUI/utilities/sanitizer.py"
	export ONCILLA_PROJECT_EXCLUDED_MODULES="pyclbr tests 001_dummy 001_migrate_3-x-x_to_4-0-0 002_migrate_4-x-x_to_4-0-2 003_migrate_4-x-x_to_4-0-3 004_migrate_4-x-x_to_4-0-7 defaultScript"

About
-----

| **Oncilla** by Thomas Mansencal – 2008 - 2014
| Copyright© 2008 - 2014 – Thomas Mansencal – `thomas.mansencal@gmail.com <mailto:thomas.mansencal@gmail.com>`_
| This software is released under terms of GNU GPL V3 license: http://www.gnu.org/licenses/
| `http://www.thomasmansencal.com/ <http://www.thomasmansencal.com/>`_
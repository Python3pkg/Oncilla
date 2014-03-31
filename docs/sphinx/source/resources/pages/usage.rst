_`Usage`
========

Once installed, you can launch **Oncilla** using this shell command::

      Oncilla

You will need to have the following environment variables defined:

-  **ONCILLA_PROJECT_DIRECTORY**: Defines the project directory you want to build the manual and **Sphinx** documentation.
-  **ONCILLA_PROJECT_NAME**: Defines the name you want to use across the manual and **Sphinx** documentation files.
-  **ONCILLA_PROJECT_PACKAGES**: Defines the packages you want to build the **Sphinx** documentation.
-  **ONCILLA_PROJECT_SANITIZER**: Defines the optional **Sphinx** documentation sanitizing **Python** module.
-  **ONCILLA_PROJECT_EXCLUDED_MODULES**: Defines the optional excluded **Python** modules from **Sphinx** documentation.
-  **ONCILLA_PROJECT_MANUAL_CSS_FILE**: Defines the optional excluded **css** stylesheet file used for the manual.

Example::

	export ONCILLA_PROJECT_DIRECTORY="/Users/kelsolaar/Documents/Development/sIBL_GUI"
	export ONCILLA_PROJECT_NAME="sIBL_GUI"
	export ONCILLA_PROJECT_PACKAGES="oncilla foundations manager umbra sibl_gui"
	export ONCILLA_PROJECT_SANITIZER="/Users/kelsolaar/Documents/Development/sIBL_GUI/utilities/sanitizer.py"
	export ONCILLA_PROJECT_EXCLUDED_MODULES="pyclbr tests 001_dummy 001_migrate_3-x-x_to_4-0-0 002_migrate_4-x-x_to_4-0-2 003_migrate_4-x-x_to_4-0-3 004_migrate_4-x-x_to_4-0-7 defaultScript"

.. raw:: html

    <br/>


#!/usr/bin/env bash

export PROJECT_DIRECTORY=$(cd $( dirname "${BASH_SOURCE[0]}" )/../../..; pwd)
export PROJECT=$( basename $PROJECT_DIRECTORY )

echo -------------------------------------------------------------------------------
echo $PROJECT - Documentation Build
echo -------------------------------------------------------------------------------

export ONCILLA_DIRECTORY=$PROJECT_DIRECTORY/utilities/Oncilla/oncilla
export HELP_DIRECTORY=$PROJECT_DIRECTORY/docs/help
export SPHINX_DIRECTORY=$PROJECT_DIRECTORY/docs/sphinx

#! Inline documentation build.
echo -------------------------------------------------------------------------------
echo Inline Documentation Build - Begin
echo -------------------------------------------------------------------------------
python $ONCILLA_DIRECTORY/reStructuredTextToHtml.py "$HELP_DIRECTORY/${PROJECT}_Manual.rst" "$HELP_DIRECTORY/${PROJECT}_Manual.html"
echo -------------------------------------------------------------------------------
echo ${PROJECT} - Inline Documentation Build - End
echo -------------------------------------------------------------------------------

#! Sphinx documentation build.
echo -------------------------------------------------------------------------------
echo Sphinx Documentation Build - Begin
echo -------------------------------------------------------------------------------
python $ONCILLA_DIRECTORY/sliceDocumentation.py "$HELP_DIRECTORY/${PROJECT}_Manual.rst" "$SPHINX_DIRECTORY/source/resources/pages"
python $ONCILLA_DIRECTORY/sliceDocumentation.py "$PROJECT_DIRECTORY/CHANGES.rst" "$SPHINX_DIRECTORY/source/resources/pages"
python $ONCILLA_DIRECTORY/buildSphinxDocumentationTocTree.py "$PROJECT" "$SPHINX_DIRECTORY/source/resources/pages/tocTree.rst" "$SPHINX_DIRECTORY/source/index.rst" "$SPHINX_DIRECTORY/source/resources/pages"
rm -rf $SPHINX_DIRECTORY/build
rm -rf $SPHINX_DIRECTORY/source/resources/packages
rm $SPHINX_DIRECTORY/source/resources/pages/api/*
rm "$SPHINX_DIRECTORY/source/resources/pages/tocTree.rst"
python $ONCILLA_DIRECTORY/buildSphinxDocumentationApi.py $( echo "${PROJECT}" | tr "[:upper:]" "[:lower:]" ) "$SPHINX_DIRECTORY/source/resources/packages" "$SPHINX_DIRECTORY/source/resources/pages/api" "$SPHINX_DIRECTORY/source/resources/pages/api.rst"
export PYTHONPATH=$SPHINX_DIRECTORY/source/resources/packages
sphinx-build -b html -d $SPHINX_DIRECTORY/build/doctrees $SPHINX_DIRECTORY/source $SPHINX_DIRECTORY/build/html
echo -------------------------------------------------------------------------------
echo Sphinx Documentation Build - End
echo -------------------------------------------------------------------------------

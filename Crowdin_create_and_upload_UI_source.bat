@echo off
REM Use this batch file to:
REM - extract translatable strings from the PrimerPrep source files (the main Python script
REM   and the glade UI definition), and put them in locale/PrimerPrep.pot
REM - extract translatable strings from the source HTML help file (in English),
REM   and put them in locale/PrimerPrepHelp.pot
REM - Post these two .pot files as well as all of the HTML help file images (Help/*.png)
REM   to Crowdin to serve as the source files for the PrimerPrep translation project
REM
REM The Crowdin configuration is found in the crowdin.yml file
REM
REM by Jeff Heath
REM Last updated: June-2024

echo Extracting the strings to translate from PrimerPrep.py
xgettext --language=Python --keyword=_ --from-code=utf-8 --output=locale\PrimerPrep.pot PrimerPrep.py
echo.

echo Extracting the translatable strings from PrimerPrep.glade
xgettext --language=Glade --keyword=translatable= --from-code=UTF-8 --join-existing --output=locale\PrimerPrep.pot PrimerPrep.glade
echo.

echo Extracting the translatable strings from PrimerPrepHelp.html
python extract_html_help_translatable_strings.py
echo.

echo Updating the UI source files (locale/PrimerPrep.pot, locale/PrimerPrepHelp.pot, Help/*.png) on Crowdin
REM The configuration of the "source:" is found in crowdin.yml
java -jar "\Program Files (x86)\CrowdinCLI\crowdin-cli.jar" upload
echo.
echo You can now update the translations in the PrimerPrep Crowdin project: https://crowdin.com/project/primerprep
echo.


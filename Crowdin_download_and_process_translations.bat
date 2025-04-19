@echo off
REM Use this batch file to download translations from Crowdin. The two .po files 
REM (PrimerPrep.po and PrimerPrepHelp.po) will be placed in subfolders of
REM locale/ by language code, e.g. locale/fr_FR/LC_MESSAGES/. The localized images
REM for the Help web page are loaded into Help/ by language code, e.g. Help/fr_FR.
REM
REM Then for EACH language sub-folder in locale/, produce a PrimerPrep.mo (compiled)
REM in the translations/ folder by language code.
REM
REM by Jeff Heath
REM Last updated: June-2024

echo Downloading the UI and Help file translations from Crowdin into the locale\ folder
REM The configuration of the "translation:" is found in crowdin.yml
java -jar "\Program Files (x86)\CrowdinCLI\crowdin-cli.jar" download
echo.

echo Creating binary (.mo) UI translation files and localized HTML help files
echo.
set "localeFolder=locale"
set "outputFolder=translations"
REM Process each translation (language) subfolder
for /d %%a in ("%localeFolder%\*") do (
  REM Note: %%a includes the folder (e.g. locale\fr_FR) while %%~naa just includes the folder name (e.g. fr_FR)
  echo Processing UI translations for %%a
  msgfmt --output-file=%outputFolder%\%%~na\LC_MESSAGES\PrimerPrep.mo %localeFolder%\%%~na\LC_MESSAGES\PrimerPrep.po
  
  echo Processing Help file translations for %%a
  python update_html_help_translatable_strings.py %%~na
)
echo.
echo All translations have been processed
echo.

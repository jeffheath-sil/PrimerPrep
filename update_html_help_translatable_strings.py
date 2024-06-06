#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# For the given language code (given on the command line), load the localized translations from
# PrimerPrepHelp.po, then scan the HTML English Help source file for translatable strings,
# marked with <span translatable="yes">...</span>, and replace them with the localized version.
# The <title>...</title> string is also localized.
#
# Several other issues are also handled, based on information loaded from the langs.json file,
# including text direction and font. These affect certain configuration settings in the HTML file.
#
import re
import os
import sys
import json

def load_translations(locale):
    """Loads translations from a PO file based on the locale."""
    po_file_path = os.path.join('locale', locale, 'LC_MESSAGES', 'PrimerPrepHelp.po')
    translations = {}
    if os.path.exists(po_file_path):
        with open(po_file_path, 'r', encoding='utf-8') as f:
            current_msgid = None
            for line in f:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                if line.startswith('#'):
                    continue  # Skip comments
                if line.startswith('msgid "') and line.endswith('"'):
                    # Extract msgid
                    current_msgid = line[7:-1]
                    # Restore any escaped special characters (backslashes or double quotes)
                    current_msgid = current_msgid.replace('\\"', '"')
                    current_msgid = current_msgid.replace('\\\\', '\\')
                elif line.startswith('msgstr "') and line.endswith('"'):
                    # Only store the translation if we have a current, valid msgid
                    if current_msgid:
                        # Extract msgstr
                        current_msgstr = line[8:-1]
                        # Restore any escaped special characters (backslashes or double quotes)
                        current_msgstr = current_msgstr.replace('\\"', '"')
                        current_msgstr = current_msgstr.replace('\\\\', '\\')
                        if (locale == 'fr_FR'):
                            # For French, we want to turn apostrophes into typographic apostrophes
                            current_msgstr = current_msgstr.replace("'", "’")
                        # Store the msgid, msgstr pair in the dictionary
                        translations[current_msgid] = current_msgstr
                        current_msgid = None  # No current entry
    return translations

def replace_translations(locale, translations, html_source, html_translation, font, text_direction):
    """Replaces translatable strings in the HTML file with translations."""
    translatable_span_pattern = r'<span\s+translatable="yes">(.+?)</span>'
    compiled_span_pattern = re.compile(translatable_span_pattern, re.DOTALL)
    image_pattern = r'(<img .+? src=")(.+?)"'
    compiled_image_pattern = re.compile(image_pattern, re.DOTALL)
    
    try:
        with open(html_source, 'r', encoding='utf-8') as f, open(html_translation, 'w', encoding='utf-8') as out:
            for line in f:
                # Check for special lines, and when found, modify appropriately
                if line.startswith('<html lang='):
                    # Just build a new version of the line
                    line = '<html lang="' + locale + '" dir="' + text_direction + '">\n'
                elif line.startswith('<title>'):
                    # Translate the title, but ignore an empty translation
                    title = translations.get('PrimerPrep Help', 'PrimerPrep Help')
                    if title:
                        line = '<title>' + title + '</title>\n'
                elif line.startswith('<body style="font-family:'):
                    if font:
                        line = line.replace("font-family:", "font-family: '" + font + "',")
                elif line.startswith('<div style="'):
                    # Float the table of contents the correct direction
                    if text_direction == 'rtl':
                        line = line.replace('float:right;', 'float:left;')
                else:
                    # Not one of the special lines, look for and replace any strings that were translated
                    matches = re.findall(compiled_span_pattern, line)
                    for match in matches:
                        translation_string = match
                        translated_text = translations.get(translation_string, translation_string)  # Get translation or use original string
                        if translated_text:
                            line = line.replace(translation_string, translated_text)
                    # Point to any replacement images that exist
                    matches = re.findall(compiled_image_pattern, line)
                    for match in matches:
                        image_filename = match[1]
                        if os.path.exists(os.path.join('Help', locale, image_filename)):
                            # This image was provided, so point to it
                            line = line.replace(image_filename, os.path.join(locale, image_filename))
                out.write(line)
    except FileNotFoundError as e:
        print("Error: HTML file not found: " + html_source)

if __name__ == '__main__':
    # Check if a command-line argument is provided
    if len(sys.argv) != 2:
        print("Usage: python update_html_help_translatable_strings.py <locale>")
        sys.exit(1)

    # Get the locale from the command-line argument
    locale = sys.argv[1]

    # Load translations from the PO file
    translations = load_translations(locale)
    
    # Load languages from .json file
    try:
        with open(os.path.join("translations", "langs.json"), 'r', encoding='utf-8') as f:
            langs = json.load(f)
        # Font name, if specified, without trailing font size
        font = re.sub(r"\s\d+$", "", langs[locale][1])
        # Text direction (should be only "ltr" or "rtl"), and make sure it is lowercase
        text_direction =  langs[locale][2].lower()
    except:
        print("Unable to process the languages file: " + os.path.join("translations", "langs.json"))
        sys.exit(1)    
    
    # Replace translatable strings with translations in the HTML file
    html_source = os.path.join("Help", "PrimerPrepHelp-en_US.htm")
    html_translation = os.path.join("Help", "PrimerPrepHelp-" + locale + ".htm")
    replace_translations(locale, translations, html_source, html_translation, font, text_direction)

    print("The translated HTML file has been saved as '" + html_translation + "'.")

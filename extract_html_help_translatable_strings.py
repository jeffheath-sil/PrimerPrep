#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Scans the Help source file for translatable strings, marked with
#    <span translatable="yes">...</span>
# and creates a .pot file which can be sent to Crowdin for translation.
# Also includes the <title>...</title> string.
#
import re

html_file = "Help\PrimerPrepHelp-en_US.htm"
pot_file = "locale\PrimerPrepHelp.pot"
pot_header = """
msgid ""
msgstr ""

"Project-Id-Version: PACKAGE VERSION\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=CHARSET\\n"
"Content-Transfer-Encoding: 8bit\\n"

"""

translatable_string_pattern = r'<span\s+translatable="yes">(.+?)</span>|<title>(.*?)</title>'
compiled_pattern = re.compile(translatable_string_pattern, re.DOTALL)

# Keep track of strings translated so we can avoid duplicate messages
translation_storage = {}

pot = open(pot_file, 'w', encoding='utf-8')
pot.write(pot_header)
with open(html_file, 'r', encoding='utf-8') as html:
    line_number = 1
    for line in html:
        matches = compiled_pattern.findall(line)  # Use findall to get all matches
        for match in matches:
            # Get the string to translate (from either the span or title expressions)
            translation_string = match[0] if match[0] else match[1]
            # Mark with the escape character any special characters (backslashes or double quotes)
            translation_string = translation_string.replace('\\', '\\\\')
            translation_string = translation_string.replace('"', '\\"')
            # only write it out if it is not a duplicate
            if translation_string not in translation_storage:
                # Write out the template for the string to translate
                pot.write('#: ' + html_file + ':' + str(line_number) + '\n')
                pot.write('msgid "' + translation_string + '"\n')
                pot.write('msgstr ""\n\n')
                # Remember this translation to avoid duplicating messages
                translation_storage[translation_string] = None
        line_number += 1

pot.close()
print(f"Help file translatable strings were written to {pot_file}")

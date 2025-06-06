#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# PrimerPrep
#
# This program is a tool that helps in preparing a primer. The
# program loads language texts, counts words and letters, and
# suggests a teaching order for introducing the letters of the
# language in a primer. It can test lesson texts for untaught
# residue. It can also produce word concordances and sequences
# of available words in a specific lesson.
#
# When run directly, this script will create and execute an instance
# of the PrimerPrepWindow class.
#
# by Jeff Heath, SIL Chad
#
# © 2025 SIL Global
#
# Modifications:
# 3.40 JCH Jun 2025
#    Mark character being taught in the list of example words in the teaching order
#    Add filter in LessonTexts, mark in bold all text that matches the filter (set to lesson letter by default)
#    In LessonTexts, mark in light yellow all words that are new (don't appear in previous lessons)
#    In glade UI, add footer under LessonText with description of markup
# 3.395 JCH May 2025
#    Fix problems in RegEx's when FreezeArabicForms has been used to prepare the data
# 3.39 JCH May 2025
#    Solidify application of new fonts, make sure on opening a project that fonts are applied completely
#    Make association of .ppdata project files with the app (w/ custom icon), to open by double-clicking
#    Clean up use of global variables - always declare them where used (even read only)
# 3.38 JCH Mar 2025
#    Verify and note input text normalization (composition NFC and NFD), if inconsistent give warning
#    Increase the dataModelVersion to 2 (as we need some normalization variables), handle loading old data
#    Decompose (NFD) all text for PrimerPrep analysis, export data consistent with input texts
#    In marking untaught residue, NFC text must be made NFD, but defer to after event handler to avoid warnings
#    In marking untaught residue, use character offsets rather than iterators
#    In TeachingOrder double-click, give message if no phrases are available
#    Instantiate the event handler (rather than just using the static class)
# 3.37 JCH Jul 2024
#    Confirm overwriting data when opening a project
# 3.36 JCH Jul 2024
#    Improve project handling - add new menus (New, Open, Save, Save As)
#    Add .ppdata extension to project file name if it's not there, but allow user to modify
#    Remove Clear Texts button, add Choose Lexicon button
# 3.35 JCH Jun 2024
#    Fix loss of affixes in display when you change UI language
#    Add Give Feedback feature (which uses a Google form) in Help menu
#    Match longer affixes before shorter ones
#    Make LoadProject more robust in error handling, prepare for loading old data models
# 3.34 JCH Jun 2024
#    Fix word counts for affixes that are analyzed separately (words with affixes were
#    overcounted, causing them to appear too early in the word Examples in the Teaching Order)
# 3.33 JCH Jun 2024
#    Some tweaks to font selection and rendering
#    Removed Auto-Search for Digraphs option from Configure menu
# 3.32 JCH May 2024
#    Returned to a flatter project directory structure
#    Help files (including en_US) now all use the %locale_with_underscore% marking
#    (Helper batch and python files now manage Crowdin integration, creation of localized Help files)
# 3.31 JCH Apr 2024
#    Fixed up some problems with the splash screen on startup
# 3.30 JCH Apr 2024
#    For concordance, turn tabs in the text into spaces (tabs are used for the columns)
# 3.29 JCH Mar 2024
#    Fixed some font issues on startup
# 3.28 JCH Mar 2024
#    Added splash screen on startup, since the startup can be quite slow at times
# 3.27 JCH Jan 2024
#    Use built-in set_do_overwrite_confirmation in chooser, since it seems to work now
#    If you choose not to overwrite, or project file name is bad, keep the save dialog open with same settings
# 3.26 JCH Jan 2024
#    Improved analysis with affixes - words with affixes weren't appearing in the Teaching Order example word list
#    Added confirmation to quit without saving if there are changes to the data
# 3.20 JCH Sep 2023-Jan 2024
#    Sort multigraphs (longest first) when processing, so that shorter don't hide longer
#    Reworked marking of untaught residue (didn't handle digraphs correctly)
#    Initial work on implementing CSS styles, handler for sight words font
#    Fix depricated use of FileChooserDialog - buttons added afterwards
#    Fixed some comments
# 3.14 JCH Mar 2022
#    Bug fix: Allow saving the teaching order right after loading from a saved project file
# 3.13 JCH Nov 2021
#    Bug fix: If first lesson is sight word, typing into its Lesson Text field causes infinite loop
# 3.12 JCH Nov 2020
#    Bug fix: Handle ugly input (combining diacritics on '-', '[' and tab)
#    Bug fix: Make sure concordance data doesn't have tabs, to confuse column output routine
# 3.11 JCH Jul 2020
#    Make script more platform-agnostic, put conditionals on Windows-specific code
# 3.10 JCH Jun 2020
#    Add help files in Dari and Pashto
# 3.05 JCH Oct 2019
#    Use Word Joiner (U+2060) instead of ZWSP (U+200B) in ZWJ attachment code
#    (ZWSP is needed for Khmer and other languages)
# 3.04 JCH Jun 2019
#    Bug fix - unbalanced paren if separate combining diacritics is checked
# 3.03 JCH Jun 2019
#    Handle input from FreezeArabicForms (ZWJs for contextual forms)
# 3.02 JCH Jun 2019
#    Make sure isRTL gets initialized, even if interface isn't set
#    Fix logger code, fix WordEdit path when there are no roots
# 3.01 JCH Jun 2019
#    Base dialogs on window not analysis object, don't show zero counts in teaching order
#    Verify data model number on project save/load, be smarter about SFM load based on markers
#    Handle change of separate combining diacritics more accurately (updates character lists)
#    Don't open sightWordsDialog if there is no row selected
# 3.00 JCH May 2019
#    Switch to Glade UI, implemented internationalization with gettext
# 2.06 JCH Apr 2019
#    After adding a sight word lesson, select that lesson to make sure it is displayed
# 2.05 JCH Apr 2019
#    Fix teachingOrder existance code
#    Add 'nj' to recommended digraphs (from Maba)
# 2.04 JCH Apr 2019
#    Fix French word-forming and word-breaking terms
# 2.03 JCH Apr 2019
#    Implement Save/Load Project
#    Fix teaching order calculation by types (words only once)
#    Fix double-click in WordList, sometimes updated wrong word
#    Fix word sort order - wasn't using the custom sort routine
# 2.02 JCH Mar 2019
#    Deactive Save Teaching Order menu item, until it makes sense
#    Manual change in word divisions also provokes recalculation of teaching order
#    On manual word divisions, get confirmation if word is too different (LevDist < 0.5)
# 2.01 JCH Mar 2019
#    Rewrote help page to reflect major changes with screen shots
#    Made draft of French help page
# 2.00 JCH Feb 2019
#    Redesigned interface with tabbed interface
#    Word Discovery tab contains all tools for defining files to load/words/affixes/breaks/digraphs/etc
#    Double-clicking a word allows manual editing of affixes (or excluding the word entirely)
#    Addition of a filter text box allows filtering/finding words in the word list
#    Allow addition of sight word "lessons" (lines) in teaching order
#    Track texts for each lesson, and show untaught residue (word-forming characters only) in red
#    Handle letters and combining marks based on unicodedata (so works better on non-Roman scripts)
# 1.04 JCH Feb 2018
#    Corrections in French help file (thanks to Dominique Henchoz)
# 1.03 JCH Feb 2018
#    Save interface selection and two configuration options to .ini file in APPDATA
#    Added French help file (.html)
#    Corrections to French interface (thanks to Dominique Henchoz)
# 1.02 JCH Feb 2018
#    Add French interface
# 1.01 JCH Feb 2018
#    Sort concordance entries so longest ones appear first
# 1.00 JCH Jan 2018
#    Add option to treat combining diacritics separately
# 0.98 JCH Nov 2017
#    Correctly processes SFMs that contain an underscore
#    Write text files with a BOM for easier identification
#    Use only spaces to separate example words in teaching order list
#       (commas considered vowel marks in Scheherazade Compact with Graphite)

APP_NAME = "PrimerPrep"
progVersion = "3.40"
progYear = "2025"
dataModelVersion = 2
DEBUG = False

import sys
import logging
logger = logging.getLogger(APP_NAME)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)
if sys.version_info[0] < 3:
    logger.error('This script requires Python 3')
    exit()
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GLib
import os
import subprocess
import platform
import re
import codecs
import unicodedata
import xml.etree.ElementTree as ET
import pickle
class UnknownProjectType(Exception):
    pass
import numpy as np
import configparser
import webbrowser
#  for internationalization
import gettext
import json

# global variable to store the program path
myGlobalProgramPath = ''
# global variable to store the current working directory path
myGlobalPath = ''
# global variable to store the current working project path
# (note that this interacts with myGlobalPath, but is not the same, as our project could be in one place - and
# we need to remember where it is! - but we might be saving word lists or teaching orders elsewhere)
myGlobalProjectPath = ''
# global variable to store the current working project name (without path, but including the .ppdata extension)
myGlobalProjectName = ''
# global instance of Renderer for managing fonts in the program (esp. TreeView)
myGlobalRenderer = None
#  global variable to hold the Glade builder - needed for loading UI elements
myGlobalBuilder = None
#  global variable to hold the event handlers
myGlobalHandler = None
# global variable to hold the main window - needed as parent for various dialogs
myGlobalWindow = None
# global variable for the interface language (English by default)
myGlobalInterface = 'en_US'
# global variable for the config file (with complete path)
myGlobalConfigFile = ''
# global variable for the config object (so we can update settings and save them out)
myGlobalConfig = configparser.ConfigParser()
# global variable for holding the page index of the GTK notebook
myGlobalNotebookPage = 0


# defaults for global CSS (Cascading Style Sheets) formatting
myGlobalCSS = """
notebook tab {
    background-color: silver;
    border: 1px black;
    border-style: solid solid none solid;
    color: gray;
}
notebook tab:hover {
    color: #606060;
}
notebook tab:checked {
    background-color: white;
    color: black;
}
"""

# present a message to the user
def SimpleMessage(title, msgType, msg):
    global myGlobalBuilder
    dlg = myGlobalBuilder.get_object('simpleMessageDialog')
    dlg.set_title(title)
    myGlobalBuilder.get_object('simpleMessageImage').set_from_icon_name(msgType, Gtk.IconSize.DIALOG)
    myGlobalBuilder.get_object('simpleMessageLabel').set_text(msg)
    dlg.show_all()
    dlg.run()
    dlg.hide()

# present a Y/N question to the user
def SimpleYNQuestion(title, msgType, msg):
    global myGlobalBuilder
    dlg = myGlobalBuilder.get_object('simpleYNQuestionDialog')
    myGlobalBuilder.get_object('simpleYNQuestionImage').set_from_icon_name(msgType, Gtk.IconSize.DIALOG)
    myGlobalBuilder.get_object('simpleYNQuestionLabel').set_text(msg)
    dlg.show_all()
    response = dlg.run()
    dlg.hide()
    return (response == 1)



class VernacularRenderer:
    '''A class used to hold vernacular font rendering information
    
    Creating an instance of this class loads the standard renderer used
    in PrimerPrep. Use SelectFont to allow the user to select/change to
    a new vernacular font. Use SetFont to apply a new vernacular font.
    
    Attributes:
      fontName (str) - current font selected for displaying vernacular text
      global_style_provider (Gtk.CssProvider) - holds global (static) CSS configuration
      vernacular_style_provider (Gtk.CssProvider) - holds CSS configuration for vernacular class
      vernFontDesc (Pango.FontDescription) - font info for vernacular text
      vernRendererText (Gtk.CellRendererText) - renderer for vernacular text
    '''
    
    def SetFont(self, fntName):
        self.fontName = fntName
        # set up the font description and CellRendererText for vernacular text in TreeViews
        self.vernFontDesc = Pango.FontDescription(self.fontName)
        self.vernRendererText.set_property('font-desc', self.vernFontDesc)
        # parse the fontName to get the family and size
        m = re.match('(.+) (\d+)$', self.fontName)
        if m:
            # set up the CSS vernacular class (which will automatically update fields with this class)
            # note that we can modify this CSS definition with different vernacular fonts 
            VernacularCSS = """
.vernacular {{
  font-family: '{}', 'Charis SIL', Ubuntu, Gentium, serif;
  font-size: {}pt;
}}""".format(m.group(1), m.group(2))
            self.vernacular_style_provider.load_from_data(bytes(VernacularCSS.encode()))
    
    def SelectFont(self):
        '''Let user select a font using the standard dialog, modify vernacular renderer.
        
        Return value: True if font was selected and changed
        '''
        global myGlobalWindow
        fontDlg = Gtk.FontChooserDialog(_("Select the font for displaying vernacular text"))
        fontDlg.set_transient_for(myGlobalWindow.window)
        fontDlg.set_font(self.fontName)
        result = fontDlg.run()
        if result == Gtk.ResponseType.OK:
            self.SetFont(fontDlg.get_font())
        fontDlg.destroy()
        return result == Gtk.ResponseType.OK
    
    def __init__(self):
        '''Initialize this Renderer object's attributes with the defaults.
        '''
        global myGlobalCSS
        # Had some difficulties with Charis SIL Semi-Condensed?
        if platform.system() == "Windows":
            fntName = "Charis SIL Semi-Condensed 14"
        else:
            fntName = "Ubuntu 14"
        #fntName = "Gentium 14"
        
        # set up the global (static) CSS provider
        self.global_style_provider = Gtk.CssProvider()
        self.global_style_provider.load_from_data(bytes(myGlobalCSS.encode()))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), self.global_style_provider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        # set up the vernacular (modifiable) CSS provider (no style yet)
        self.vernacular_style_provider = Gtk.CssProvider()
        #self.vernacular_style_provider.load_from_data(bytes(VernacularCSS.encode()))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), self.vernacular_style_provider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        # create the CellRendererText for vernacular text in TreeViews
        self.vernRendererText = Gtk.CellRendererText()
        
        # set the font for the FontDescription/CellRendererText and the VernacularCSS
        self.SetFont(fntName)


class AffixesDialog:
    '''A class used to present a dialog for specifying the affixes in the language.
    
    Attributes:
      dialog (Dialog object) - dialog for managing word-breaking/forming chars
    '''
    
    def __init__(self):
        '''Prepare dialog for defining affixes, for running later.'''
        global myGlobalBuilder
        
        self.dialog = myGlobalBuilder.get_object('affixesDialog')
        self.textview = myGlobalBuilder.get_object('affixesDialogTextView')
        # set up the textview to use the vernacular font
        self.textview.get_style_context().add_class("vernacular")
        # monitor keypresses so we can close the dialog on Enter
        self.textview.connect('key-press-event', self.on_keyPress)
    
    def Run(self):
        self.textview.grab_focus()
        self.textview.get_buffer().place_cursor(self.textview.get_buffer().get_end_iter())
        self.dialog.show_all()
        response = self.dialog.run()
        # don't hide the dialog yet, as we run it until valid or cancel
        #self.dialog.hide()
        return (response == 1)
    
    def SetAffixes(self, affixes):
        # put the affix list into the textview
        buf = self.textview.get_buffer()
        buf.set_text(' '.join(affixes))
    
    def GetAffixes(self):
        buf = self.textview.get_buffer()
        txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)
        return txt
    
    def on_keyPress(self, widget, event):
        if event.get_keycode()[1] == 13:
            # Enter was typed, click OK
            self.dialog.activate_default()
            return True
        return False


class WordBreaksDialog:
    '''A class used to present a dialog for specifying the
    word-breaking and word-forming characters in the language.
    
    Attributes:
      dialog (Dialog object) - dialog for managing word-breaking/forming chars
      wordBreakStore (listStore) - data store for word breaking chars
      wordFormStore (listStore) - data store for word forming chars
    '''
    
    def __init__(self):
        '''Prepare dialog for defining word breaking/forming characters, for running later.'''
        global myGlobalBuilder
        #global myGlobalRenderer
        
        self.dialog = myGlobalBuilder.get_object('wordBreaksDialog')
        self.wordBreakStore = myGlobalBuilder.get_object('wordBreakListStore')
        self.wordBreakTreeView = myGlobalBuilder.get_object('wordBreakTreeView')
        #column = myGlobalBuilder.get_object('wordBreakColumn')
        #column.set_cell_data_func(myGlobalRenderer.vernRendererText, None)
        
        #Gtk.TreeViewColumn(_("Word-Breaking"), myGlobalRenderer.vernRendererText, text=0)
        #wordBreakTreeView.append_column(column)
        
        # put in ascending letter order
        self.wordBreakStore.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        self.wordBreakTreeView.connect("row-activated", self.on_WordBreak_doubleClick)
        
        self.wordFormStore = myGlobalBuilder.get_object('wordFormListStore')
        self.wordFormTreeView = myGlobalBuilder.get_object('wordFormTreeView')
        #column = myGlobalBuilder.get_object('wordFormColumn')
        #column = Gtk.TreeViewColumn(_("Word-Forming"), myGlobalRenderer.vernRendererText, text=0)
        #self.wordFormTreeView.append_column(column)
        
        # put in ascending letter order
        self.wordFormStore.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        self.wordFormTreeView.connect("row-activated", self.on_WordForm_doubleClick)
    
    def Run(self, wordBreakChars, wordFormChars):
        global myGlobalBuilder
        global myGlobalRenderer
        
        # make sure TreeViews are using current vernacular font
        myGlobalBuilder.get_object('wordBreakCellRenderer').set_property('font-desc', myGlobalRenderer.vernFontDesc)
        myGlobalBuilder.get_object('wordFormCellRenderer').set_property('font-desc', myGlobalRenderer.vernFontDesc)
        # clear the store and add each of the letters in the wordBreakChars list
        self.wordBreakStore.clear()
        for letter in wordBreakChars:
            if letter != ' ' and letter != '\xa0':
                # don't add the space or non-breaking space - they always word break, so hide
                dispLetter = letter
                # if the first character is a combining diacritic
                if unicodedata.category(dispLetter[0]) == 'Mn':
                    # then prepend the dotted circle base character
                    dispLetter = '\u25CC' + dispLetter
                self.wordBreakStore.append([dispLetter])
        
        # clear the store and add each of the letters in the wordFormChars list
        self.wordFormStore.clear()
        for letter in wordFormChars:
            dispLetter = letter
            # if the first character is a combining diacritic
            if unicodedata.category(dispLetter[0]) == 'Mn':
                # then prepend the dotted circle base character
                dispLetter = '\u25CC' + dispLetter
            self.wordFormStore.append([dispLetter])
        
        self.dialog.show_all()
        response = self.dialog.run()
        self.dialog.hide()
        return (response == 1)
    
    def on_WordBreak_doubleClick(self, widget, row, col):
        '''Shift the activated letter to the word-forming (non-break) list
        
        Parameters: widget, row - for accessing the active row in the TreeView
        '''
        model = widget.get_model()
        # Get the letter for this row
        letter = model[row][0]
        # remove this letter from the breaking list and add it to the forming list
        self.wordBreakStore.remove(model[row].iter)
        self.wordFormStore.append([letter])
        # make sure it is selected and visible
        for row in self.wordFormStore:
            if row[0] == letter:
                self.wordFormTreeView.get_selection().select_path(row.path)
                self.wordFormTreeView.scroll_to_cell(row.path)
                break
    
    def on_WordForm_doubleClick(self, widget, row, col):
        '''Shift the activated letter to the word-breaking list
        
        Parameters: widget, row - for accessing the active row in the TreeView
        '''
        model = widget.get_model()
        # Get the letter for this row
        letter = model[row][0]
        # remove this letter from the forming list and add it to the breaking list
        self.wordFormStore.remove(model[row].iter)
        self.wordBreakStore.append([letter])
        # make sure it is selected and visible
        for row in self.wordBreakStore:
            if row[0] == letter:
                self.wordBreakTreeView.get_selection().select_path(row.path)
                self.wordBreakTreeView.scroll_to_cell(row.path)
                break
    
    def GetWordBreakChars(self):
        chars = []
        for row in self.wordBreakStore:
            letter = row[0]
            if letter[0] == '\u25CC':
                # remove dotted circle base before a combining diacritic
                letter = letter[1:]
            chars.append(letter)
        return chars
    
    def GetWordFormChars(self):
        chars = []
        for row in self.wordFormStore:
            letter = row[0]
            if letter[0] == '\u25CC':
                # remove dotted circle base before a combining diacritic
                letter = letter[1:]
            chars.append(letter)
        return chars
        

class DigraphsDialog:
    '''A class used to present a dialog for specifying the digraphs in the language.
    
    Attributes:
      dialog (Dialog object) - dialog for entering diagraphs (and multigraphs)
      textview (TextView object) - text field where user types/edits digraph list
    '''
    
    def __init__(self):
        '''Prepare dialog for defining digraphs, for running later.'''
        global myGlobalBuilder
        
        # keep track of some builder UI objects
        self.dialog = myGlobalBuilder.get_object('digraphsDialog')
        self.textview = myGlobalBuilder.get_object('digraphsDialogTextView')
        # set up the textview to use the vernacular font
        self.textview.get_style_context().add_class("vernacular")
        # monitor keypresses so we can close the dialog on Enter
        self.textview.connect('key-press-event', self.on_keyPress)
    
    def Run(self):
        self.textview.grab_focus()
        self.textview.get_buffer().place_cursor(self.textview.get_buffer().get_end_iter())
        response = self.dialog.run()
        # don't hide the dialog yet, as we run it until valid or cancel
        #self.dialog.hide()
        return (response == 1)
    
    def SetDigraphs(self, digraphs):
        # put the digraph list into the textview
        buf = self.textview.get_buffer()
        buf.set_text(' '.join(digraphs))
    
    def GetDigraphs(self):
        # get the digraph list (as text) from the textview
        buf = self.textview.get_buffer()
        txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)
        return txt
    
    def on_keyPress(self, widget, event):
        if event.get_keycode()[1] == 13:
            # Enter was typed, click OK
            self.dialog.activate_default()
            return True
        return False


class WordEditDialog:
    '''WordEditDialog - class to create and run a dialog to edit word info.
    
    Creating an instance of this class creates a dialog which presents
    a concordance view of the given data. Each line of the data should contain
    2 tabs, separating the data into 3 columns: prefix, item, postfix. In this
    way the item being concorded can be aligned in the middle column. A label is
    also passed in the __init__ method, so that information on what is being
    concorded can be displayed.
    
    Attributes:
      dialog (Dialog object) - dialog for displaying the concordance
      excludeWord (CheckButton object) - checked if the word should be excluded
      divideView (TextView object) - text field where user edits word divisions
      concordanceListStore (ListStore object) - list that holds the concordance
    '''

    def __init__(self):
        '''Prepare dialog for editing individual words, for running later.'''
        global myGlobalBuilder
        
        # keep track of some builder UI objects
        self.dialog = myGlobalBuilder.get_object("wordEditDialog")
        self.excludeWord = myGlobalBuilder.get_object("excludeWordCheckButton")
        self.divideView = myGlobalBuilder.get_object("divideWordTextView")
        self.divideBuffer = myGlobalBuilder.get_object("divideWordTextBuffer")
        self.concordanceListStore = myGlobalBuilder.get_object("concordanceListStore")
        # set up the textview to use the vernacular font
        self.divideView.get_style_context().add_class("vernacular")
        # monitor clicks of the exclude CheckButton
        self.excludeWord.connect("clicked", self.on_ExcludeWord_click)
        # monitor keypresses so we can close the dialog on Enter
        self.divideView.connect('key-press-event', self.on_keyPress)
    
    def Run(self, word, affix_word, wordExcluded, data):
        '''Run dialog for editing a word and displaying a concordance.
        
        Parameters: word (str) - word to edit (no formatting)
                    affix_word (str) - word with affixes marked, e.g. re- work -ing
                    wordExcluded (bool) - set if the word was marked as excluded
                    data (str) - multiline string of prefix \t item \t postfix
        '''
        global myGlobalBuilder
        global myGlobalRenderer
        global myGlobalWindow
        
        # make sure TreeView columns are using current font
        myGlobalBuilder.get_object('wordConcordPreCellRenderer').set_property('font-desc', myGlobalRenderer.vernFontDesc)
        myGlobalBuilder.get_object('wordConcordWordCellRenderer').set_property('font-desc', myGlobalRenderer.vernFontDesc)
        myGlobalBuilder.get_object('wordConcordPostCellRenderer').set_property('font-desc', myGlobalRenderer.vernFontDesc)
        
        label = '<b>' + _("Indicate how you want to analyze the word: '{}'").format(word) + '</b>'
        myGlobalBuilder.get_object('wordEditDialogLabel').set_markup(label)
        self.excludeWord.set_active(wordExcluded)
        self.divideBuffer.set_text(affix_word)
        
        self.concordanceListStore.clear()
        if len(data) > 0:
            # we will need the data split into lines
            lines = re.split('\n', data)
            
            # create the label with the number of occurrences
            label = _("Concordance of the word: <b>{}</b>").format(word)
            if myGlobalWindow.isRTL:
                label += '\u200f'
            label += _(" ({} occurrences)").format(len(lines))
            myGlobalBuilder.get_object('wordConcordanceLabel').set_markup(label)
            
            # populate the list store with the concordance data
            for line in lines:
                preword, word, postword = re.split('\t', line)
                self.concordanceListStore.append([preword, word, postword])
        
        # make sure concordance is scrolled to the top
        myGlobalBuilder.get_object('wordEditScrolledWindow').get_vadjustment().set_value(0)
        
        response = self.dialog.run()
        # don't hide the dialog yet, as we run it until valid or cancel
        #self.dialog.hide()
        return (response == 1)
    
    def on_ExcludeWord_click(self, button):
        '''Toggle the check box for excluding the word.
        
        Parameters: button (unused)
        '''
        self.divideView.set_editable(not self.excludeWord.get_active())
        self.divideView.set_cursor_visible(not self.excludeWord.get_active())
        self.divideView.set_opacity(1.0 - float(self.excludeWord.get_active()) / 2)

    def on_keyPress(self, widget, event):
        if event.get_keycode()[1] == 13:
            # Enter was typed, click OK
            self.dialog.activate_default()
            return True
        return False


class ConfigureSFMDialog:
    '''A dialog class used collect user preferences for handling SFM files.
    
    Attributes:
      dialog (Dialog object) - dialog for managing SFM handling preferences
      btnProcessSFMs (RadioButton object) - tells us to process SFMs
      btnIgnoreSFMs (RadioButton object) - tells us to ignore certain SFMs
      textIgnoreSFMs (Entry object) - text field of SFMs to ignore
      btnOnlySFMs (RadioButton object) - tells us to only process certain SFMs
      textOnlySFMs (Entry object) - text field of only SFMs to process
      btnDontProcessSFMs (RadioButton object) - tells us to ignore SFMs
    '''
    
    def __init__(self):
        global myGlobalBuilder
        
        # keep track of some builder UI objects
        self.dialog = myGlobalBuilder.get_object('configureSFMDialog')
        self.textview = myGlobalBuilder.get_object('configureSFMTextView')
        self.textbuffer = myGlobalBuilder.get_object('configureSFMTextBuffer')
        self.removeButton = myGlobalBuilder.get_object("configureSFMRemoveButton")
        self.ignoreButton = myGlobalBuilder.get_object("configureSFMIgnoreButton")
        self.processButton = myGlobalBuilder.get_object("configureSFMProcessButton")
        self.ignoreEntry = myGlobalBuilder.get_object("configureSFMIgnoreEntry")
        self.processEntry = myGlobalBuilder.get_object("configureSFMProcessEntry")
        # set up the textview to use the vernacular font
        self.textview.get_style_context().add_class("vernacular")
    
    def Run(self, introText, initIgnoreLines, initProcessLines):
        self.textbuffer.set_text(introText)
        self.ignoreEntry.set_text(initIgnoreLines)
        self.processEntry.set_text(initProcessLines)
        self.dialog.run()
        self.dialog.hide()


class ConcordanceDialog:
    '''A class to create and run a dialog to show a concordance.
    
    Creating an instance of this class creates and runs a dialog which presents
    a concordance view of the given data. Each line of the data should contain
    2 tabs, separating the data into 3 columns: prefix, item, postfix. In this
    way the item being concorded can be aligned in the middle column. A label is
    also passed in the __init__ method, so that information on what is being
    concorded can be displayed.
    
    Attributes:
      dialog (Dialog object) - dialog for displaying the concordance
    '''

    def __init__(self):
        global myGlobalBuilder
        
        # keep track of some builder UI objects
        self.dialog = myGlobalBuilder.get_object('concordanceDialog')
    
    def Run(self, letter, data):
        '''Run a concordance dialog to display the given data.
        
        Parameters: letter (str) - letter in the teaching order for the concordance
                    data (str) - multiline string of prefix \t item \t postfix
        '''
        global myGlobalBuilder
        global myGlobalRenderer
        global myGlobalWindow
        
        # make sure TreeView columns are using current font
        myGlobalBuilder.get_object('concordancePreCellRendererText').set_property('font-desc', myGlobalRenderer.vernFontDesc)
        myGlobalBuilder.get_object('concordanceWordCellRendererText').set_property('font-desc', myGlobalRenderer.vernFontDesc)
        myGlobalBuilder.get_object('concordancePostCellRendererText').set_property('font-desc', myGlobalRenderer.vernFontDesc)
        
        # we will need the data split into lines
        lines = re.split('\n', data)
        
        # create the label with the number of occurrences
        label = _("Text fragments available (from your loaded texts) in the lesson for '{}'").format(letter)
        if myGlobalWindow.isRTL:
            label += '\u200f'
        label += _(" ({} occurrences)").format(len(lines))
        myGlobalBuilder.get_object('concordanceDialogLabel').set_text(label)
        
        # populate the list store with the data parameter
        listStore = myGlobalBuilder.get_object("concordanceListStore")
        listStore.clear()
        for line in lines:
            preword, word, postword = re.split('\t', line)
            listStore.append([preword, word, postword])
        
        # make sure concordance is scrolled to the top
        myGlobalBuilder.get_object('concordanceScrolledWindow').get_vadjustment().set_value(0)
        
        self.dialog.run()
        self.dialog.hide()


class SightWordsDialog:
    '''A class used to present a dialog for specifying sight words.
    
    Attributes:
      dialog (Dialog object) - dialog for managing sight word entry
      textview (TextView object) - text field where user types/edits digraph list
    '''
    
    def __init__(self):
        '''Prepare dialog for defining digraphs, for running later.'''
        global myGlobalBuilder
        
        # keep track of some builder UI objects
        self.dialog = myGlobalBuilder.get_object('sightWordsDialog')
        self.textview = myGlobalBuilder.get_object('sightWordsDialogTextView')
        self.textbuf = myGlobalBuilder.get_object('sightWordsTextBuffer')
        # set up the textview to use the vernacular font
        self.textview.get_style_context().add_class("vernacular")
        # monitor keypresses so we can close the dialog on Enter
        self.textview.connect('key-press-event', self.on_keyPress)
    
    def Run(self):
        self.textview.grab_focus()
        self.textbuf.place_cursor(self.textbuf.get_end_iter())
        response = self.dialog.run()
        self.dialog.hide()
        return (response == 1)
    
    def SetSightWords(self, sightWords):
        buf = self.textview.get_buffer()
        buf.set_text(' '.join(sightWords))
    
    def GetSightWords(self):
        # get the sight words list (as text) from the textview
        buf = self.textview.get_buffer()
        txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)
        return txt
    
    def on_keyPress(self, widget, event):
        if event.get_keycode()[1] == 13:
            # Enter was typed, click OK
            self.dialog.activate_default()
            return True
        return False


class WordAnalysis:
    '''A class used to load/process/hold word analysis info
    
    Attributes: described in the comments of the __init__ method.'''

    def AddWordsFromFile(self, file):
        '''Load all lines from the given text file and store them in the class
        object. Consider whether file is an SFM file, and handle it properly.
        Once data is loaded, send it to FindWords to add word data to object.
        
        Parameter: file (str) - file name and path of file to check
        Return value: True if the file was loaded without error
        '''
        # check if this is an SFM file, configure if not done yet
        isSFMFile = self.CheckIfSFM(file)
        
        # load in entire file in 'lines' list, processing SFMs as we go
        lines = []
        try:
            f = codecs.open(file, 'r', encoding='utf-8')
            firstline = True
            prevLineRemoved = False
            for line in f:
                if firstline:
                    # get rid of any Unicode BOM at the beginning of the file
                    line = re.sub('^\ufeff', '', line)
                    firstline = False
                
                if isSFMFile and not re.match(r'^\\', line) and len(lines)>0:
                    # no SFM on this line
                    if not prevLineRemoved:
                        # attach to previous (with SFM) line
                        lines[-1] = lines[-1] + ' ' + line.strip()
                else:
                    prevLineRemoved = False
                    if self.sfmProcessSFMs:
                        # remove certain SFM markers/lines in text
                        if len(self.sfmIgnoreLines) > 0:
                            if re.match(r'\\(' + self.sfmIgnoreLines + ')( |\n)', line):
                                # remove entire line including text for certain SFMs
                                line = ''
                        # keep only certain SFM markers/lines in text
                        if len(self.sfmOnlyLines) > 0:
                            if not re.match(r'\\(' + self.sfmOnlyLines + ')( |\n)', line):
                                # this SFM is not a keeper so remove entire line including text
                                line = ''
                        line = re.sub(r'\\\w+', '', line)  # remove any other SFMs
                    line = line.strip()  # remove leading/trailing spaces
                    # check to see if we have anything left in the line
                    if len(line) > 0:
                        # append the line to the list of lines
                        lines.append(line)
                    else:
                        prevLineRemoved = True
            f.close()
        except Exception:
            title = _("File error")
            msg = _("Error. File could not be read.")
            SimpleMessage(title, 'dialog-information', msg)
            return False
        
        # check the lines for encoding errors
        self.CheckEncoding(lines)
        
        # convert this new data (from the file just loaded) to NFD encoding
        lines = [unicodedata.normalize('NFD', line) for line in lines]
        
        # store the file name/path, and all the lines in the file
        self.fileNames.append(file)
        self.fileLines.append(lines)
        
        # process the lines to find the characters and words
        self.FindChars(lines)
        self.FindWords(lines)
        return True
    
    def CheckEncoding(self, lines):
        '''Check the encoding of the given lines.
        
        Check for the presence of composed/decomposed characters. If inconsistent, warn the user
        and offer to convert everything to decomposed.
        
        Parameter: lines (list of str) - lines of text to be analyzed
        '''
        if self.userInformedEncodingError:
            # user already knows that data is inconsistent, and has made a choice about decomposition
            return
        
        # scan through the lines looking for composed and decomposed characters
        for line in lines:
            if not self.containsNFC and line != unicodedata.normalize('NFD', line):
                self.containsNFC = True
            if not self.containsNFD and line != unicodedata.normalize('NFC', line):
                self.containsNFD = True
            if self.containsNFC and self.containsNFD:
                # exit the loop early if both flags are set
                break
        
        # if we have inconsistent encoding, and user hasn't been informed, then inform the user
        if self.containsNFC and self.containsNFD and not self.userInformedEncodingError:
            title = _("Encoding error")
            msg = _("""Warning: Your input data has inconsistent encoding, with some characters composed
and some decomposed. This is likely due to using different keyboards to type the data.
Your original files will NOT be modified, but you should ask a consultant to help you
make your data more consistent. Any outputs from PrimerPrep (word list, teaching order)
will be output in decomposed format.""")
            SimpleMessage(title, 'dialog-warning', msg)
            self.userInformedEncodingError = True
    
    def CheckIfSFM(self, file):
        '''Check if the file is an SFM file, and configure appropriately.
        
        Parameter: file (str) - file name and path of file to check
        Return value: True if the file is an SFM file
        '''
        global myGlobalWindow
        # assume we won't process SFMs
        self.sfmProcessSFMs = False
        try:
            f = codecs.open(file, 'r', encoding='utf-8')
            combinedLines = ""
            line = f.readline()
            # get rid of BOM from beginning of file, if present
            line = re.sub('^\ufeff', '', line)
            countSFMs = 0
            markers = []
            for i in range(10):
                combinedLines = combinedLines + line[0:40]
                if combinedLines[-1] != "\n":
                    # we only got part of the line, so put in ellipsis and end of line
                    if combinedLines[-1] != "\r":
                        # put in ellipsis except special case where we got \r of \r\n
                        combinedLines = combinedLines + '...'
                    combinedLines = combinedLines + '\n'
                m = re.match(r'\\(\w*) ', line)
                if m:
                    # line begins with backslash so we assume it is an SFM; count it
                    countSFMs = countSFMs + 1
                    markers.append(m.group(1))
                # get the next line; if file is short, resulting empty string should be OK
                line = f.readline()
            f.close()
        except Exception:
            return False
        
        # remove newline from the end
        combinedLines = combinedLines[:-1]
        # consider the file an SFM file if it has at least 4 lines that start with '\'
        if countSFMs > 4:
            isSFMFile = True
        else:
            isSFMFile = False
        # We used to only configure once, but it might be a different kind of SFM file (Scripture vs lexicon)
        # so run configuration every time we find an SFM file
        if isSFMFile:
            # this is an SFM file
            if 'lx' in markers:
                self.sfmIgnoreLines = ''
                self.sfmProcessLines = 'lx|pdv|xv'
                myGlobalWindow.theConfigureSFMDialog.removeButton.set_active(True)
                myGlobalWindow.theConfigureSFMDialog.processButton.set_active(True)
            elif 'h' in markers or 'toc1' in markers or 'mt1' in markers:
                self.sfmIgnoreLines = 'id|rem|restore|h|toc1|toc2|toc3'
                self.sfmProcessLines = ''
                myGlobalWindow.theConfigureSFMDialog.removeButton.set_active(True)
                myGlobalWindow.theConfigureSFMDialog.ignoreButton.set_active(True)
            
            # run the dialog
            initIgnoreLines = self.sfmIgnoreLines.replace('|',' ')
            initProcessLines = self.sfmProcessLines.replace('|', ' ')
            myGlobalWindow.theConfigureSFMDialog.Run(combinedLines, initIgnoreLines, initProcessLines)
            self.sfmProcessSFMs = myGlobalWindow.theConfigureSFMDialog.removeButton.get_active()
            if self.sfmProcessSFMs:
                # user chose to remove SFMs
                if myGlobalWindow.theConfigureSFMDialog.ignoreButton.get_active():
                    # user chose to ignore certain SFMs, keep the list
                    text = myGlobalWindow.theConfigureSFMDialog.ignoreEntry.get_text()
                    text = text.strip()
                    markers = re.split(r'\s+', text)
                    self.sfmIgnoreLines = '|'.join(markers)
                    self.sfmOnlyLines = ''
                else:
                    # user chose to only process certain SFMs, keep the list
                    text = myGlobalWindow.theConfigureSFMDialog.processEntry.get_text()
                    text = text.strip()
                    markers = re.split(r'\s+', text)
                    self.sfmOnlyLines = '|'.join(markers)
                    self.sfmIgnoreLines = ''
        return isSFMFile
    
    def FindChars(self, lines):
        '''Takes a list of lines and for each line, check each character
        (making sure to combine diacritics or not) and record it as
        word forming or word breaking.
        
        Parameter: lines (list of str) - lines of text to be analyzed
        '''
        # build a RegEx that splits out individual characters
        # (built outside loop because it is the same for every line)
        # make sure to attach any zero width joiners (ZWJs U+200d)
        # but remove/ignore Word Joiners (WJs U+2060) - they are only there
        # to ensure that the ZWJs get attached to the right character
        if self.separateCombDiacritics:
            # RegEx that treats combining diacritics separately
            findChars = re.compile(r'(\u200d?[^\u2060]\u200d?)')
        else:
            # RegEx that includes combining diacritics with their preceding base characters
            findChars = re.compile(r'(\u200d?[^\u2060][\u0300-\u036f]*\u200d?)')
        
        # make sure we have identified all characters in the file
        for line in lines:
            # check all characters in line and if not seen before, add it
            # to word forming or breaking list (based on unicodedata.category)
            for char in re.findall(findChars, line):
                if ord(char[-1]) in range(0x300, 0x36f):
                    # last character is a combining diacritic
                    #  get base character
                    ch = char[0]
                    if ch == '\u200d':
                        # skip over initial ZWJ, if present
                        ch = char[1]
                    if unicodedata.category(ch)[0] not in 'LM':
                        # base is not a letter or a mark
                        # just ignore it for building the character list
                        # this addresses problems like when the base character is '-' or ']', messing up regexes
                        char = ' '
                if char not in self.chars:
                    # this char has not been seen yet, mark as seen
                    self.chars[char] = 1
                    ch = char[0]
                    if ch == '\u200d':
                        # if it's a ZWJ, get the next letter
                        ch = char[1]
                    # add to either word forming/breaking character list
                    if unicodedata.category(ch)[0] in 'LM':
                        # only letters or combining marks
                        self.wordFormChars.append(char)
                    else:
                        #  this would include punctuation, symbols, spaces, control codes
                        self.wordBreakChars.append(char)
    
    def FindWords(self, lines):
        '''Takes a list of lines and for each line, break it into words which
        are added into the words dictionary (which keeps a frequency count).
        
        Parameter: lines (list of str) - lines of text to be analyzed
        '''
        # build 'breaks' string with all word breaking characters for RegEx splitting
        breaks = ''
        for char in self.wordBreakChars:
            # need to put '\' before special characters
            if char in '.^$*+-?{}\\[]|()':
                breaks = breaks + '\\'
            breaks = breaks + char
        
        kWordCnt = 0
        kWordManual = 1
        kWordExclude = 2
        kWordAffixForm = 3
        kWordMarkupForm = 4
        # process each line individually
        for line in lines:
            # make list of words split by spaces, punctuation, other word break chars
            linewords = re.split('[\\s' + breaks + ']+', line)
            for word in linewords:
                #logger.debug('"', repr(word), '"')
                if (len(word) == 0) or re.match(r'^[-\d]+$', word):
                    # this word is empty or just numbers/hyphens, skip to next word
                    continue
                word = word.lower()
                if word in self.words:
                    # we've already seen this word, just increase its count
                    self.words[word][kWordCnt] += 1
                else:
                    # first time to see this word, set count to 1, set defaults for all other list fields
                    self.words[word] = [1, False, False, word, '<b>' + word + '</b>']
        
        # process the affixes as well, if any; also sets teachingOrderChanged to True to force recalculating teaching order
        self.ProcessAffixes()
    
    
    def GetNumFiles(self):
        '''Returns the current number of texts in the WordAnalysis object
        '''
        return len(self.fileNames)
    
    def GetNumWords(self):
        '''Returns the current number of words in the WordAnalysis object
        '''
        return len(self.words)
    
    def UpdateFileList(self, listStore, fullPath):
        '''Update the file list in the listStore provided to reflect the current
        list of files in the WordAnalysis object.
        
        Parameter: listStore (ListStore object) - data storage for current word list
                   fullPath (Boolean) - True if full path should be shown
        '''
        # start by clearing the list
        listStore.clear()
        
        # add each of the words and its count
        for fileName in self.fileNames:
            if fullPath:
                name = fileName
            else:
                name = fileName.split('\\')[-1]
            listStore.append([name])
    
    def UpdateWordList(self, listStore):
        '''Update the word list in the listStore provided to reflect the current
        list of words in the WordAnalysis object.
        
        Parameter: listStore - data storage for current word list
        '''
        # start by clearing the list
        listStore.clear()
        
        kWordCnt = 0
        kWordManual = 1
        kWordExclude = 2
        kWordAffixForm = 3
        kWordMarkupForm = 4
        # add each of the words and its count
        for word, word_info in self.words.items():
            # put zero-width space in front, or markup may not appear
            markup_word = '\u200B' + word_info[kWordMarkupForm]
            listStore.append([markup_word, word_info[kWordCnt], word])
        # start with descending count order
        # (but user can sort by clicking column headers)
        listStore.set_sort_column_id(1, Gtk.SortType.DESCENDING)
    
    def CalculateTeachingOrder(self, excludeAffixes, countWords):
        '''Using the list of words in this WordAnalysis class object,
        make sure we have broken all words into a list of graphemes and
        then calculate the teaching order of the graphemes.
        
        Parameter: excludeAffixes (bool) - True if we exclude affixes, False if they are counted as words
                   countWords (bool) - True if we count all words (tokens), False if we count words only once (types)
        '''
        #
        # Clear all data on teaching order and on how words split into graphemes in this WordAnalysis object.
        #
        
        # The morphemes are used to do the teaching order calculation,
        # but the actual word graphemes must be used to determine the example words
        # wordsAsGraphemes: dict of { word, list of graphemes in word }
        self.wordsAsGraphemes = {}
        # morphemesAsGraphemes: dict of { morpheme, list of graphemes in morpheme }
        self.morphemesAsGraphemes = {}
        # analysisWords: dict of { word, word count in all texts }
        self.analysisWords = {}
        # analysisMorphemes: dict of { morpheme, morpheme count in all texts }
        self.analysisMorphemes = {}
        
        # graphemeUse: dict of { grapheme, grapheme count in all texts }
        self.graphemeUse = {}
        # teachingOrder: list of graphemes (letters) in order to present in teaching
        #   numbers in this list indicate sight word entries, with number being index (plus one) to list
        self.teachingOrder = []
        # sightWords: list of lists of sight words
        self.sightWords = []
        # graphemeExampleWords: dict of { grapheme, list of sample words to introduce the grapheme }
        self.graphemeExampleWords = {}
        
        # we generally want to keep our sample lesson texts, stored in the lessonTexts dictionary by grapheme
        # but since we deleted any sight word lessons, we need to remove the texts connected to sight word lessons
        # we work from a list of the keys, so that as we delete dictionary entries, we aren't disturbing the loop
        for gr in list(self.lessonTexts.keys()):
            if isinstance(gr, int):
                # remove this sight word lesson text
                del self.lessonTexts[gr]
        
        if len(self.words) == 0:
            # no words to process
            return
        
        # convert the digraphs list into a RegEx OR group
        digraphList = self.digraphs
        # make sure that the longer multigraphs come first, or they might not get matched
        digraphList.sort(key=len, reverse=True)
        # build the RegEx string (escape any special characters - which would be weird, but for safety)
        digraphStr = '|'.join(re.escape(dg) for dg in digraphList)
        if len(digraphStr) > 0:
            digraphStr += '|'
        
        # build a RegEx that can split out individual graphemes including digraphs (from list)
        # (built outside loop because it is the same for every word)
        # make sure to include any zero width joiners (ZWJs, \u200d), but exclude word joiners 
        # (WJs, \u2060) and any zero width spaces (ZWSPs, \u200b) which are used to mark affixes
        if self.separateCombDiacritics:
            # RegEx that treats combining diacritics separately
            findGraphemes = re.compile(r'(\u200d?(?:' + digraphStr + r'[^\u200b\u2060])\u200d?)')
        else:
            # RegEx that includes combining diacritics with their preceding base characters
            findGraphemes = re.compile(r'(\u200d?(?:' + digraphStr + r'[^\u200b\u2060])[\u0300-\u036f]*\u200d?)')
        
        kWordCnt = 0
        kWordManual = 1
        kWordExclude = 2
        kWordAffixForm = 3
        kWordMarkupForm = 4
        
        for word, word_info in self.words.items():
            # decompose this word as a list of graphemes to determine the example words 
            # (morphemes are used for the Teaching Order calculations)
            self.wordsAsGraphemes[word] = re.findall(findGraphemes, word)
            # put the word count into the analysisWords dictionary (zero if this word is excluded)
            if not word_info[kWordExclude]:
                self.analysisWords[word] = (word_info[kWordCnt] if countWords else 1)
            else:
                self.analysisWords[word] = 0
            
            # process the individual affixes of this word
            affixList = word_info[kWordAffixForm].split(' ')
            for morph in affixList:
                # process each affix or root
                if (not excludeAffixes) or (not morph.endswith('-') and not morph.startswith('-')):
                    # either we aren't excluding affixes, or this isn't an affix
                    if not word_info[kWordExclude]:
                        # store this "word", with its count (adding to existing one if found)
                        self.analysisMorphemes[morph] = \
                            self.analysisMorphemes.get(morph, 0) + (word_info[kWordCnt] if countWords else 1)
                    else:
                        # don't count the graphemes of excluded words, but make sure it's in the word list (with zero count)
                        if morph not in self.analysisMorphemes:
                            self.analysisMorphemes[morph] = 0
                    
                    morphNoHyphen = morph
                    if morphNoHyphen.endswith('-') or morphNoHyphen.startswith('-'):
                        # this is an affix, so remove the hyphen before splitting into graphemes
                        morphNoHyphen = morphNoHyphen.replace('-', '')
                    
                    # retrieve a list of graphemes for this morpheme
                    if morph in self.morphemesAsGraphemes:
                        # just load the graphemes that were generated before
                        graphemes = self.morphemesAsGraphemes[morph]
                    else:
                        # generate and store the graphemes for this morpheme
                        graphemes = re.findall(findGraphemes, morphNoHyphen)
                        self.morphemesAsGraphemes[morph] = graphemes
                    for grapheme in graphemes:
                        if not word_info[kWordExclude]:
                            # increase count of uses for this grapheme by num of words
                            # (if first time, get default 0 then add num of words)
                            self.graphemeUse[grapheme] = \
                                self.graphemeUse.get(grapheme, 0) + (word_info[kWordCnt] if countWords else 1)
                        else:
                            # just make sure the grapheme is in the graphemeUse dictionary
                            if grapheme not in self.graphemeUse:
                                self.graphemeUse[grapheme] = 0
        
        teachingOrderAlgorithm = "elimination"
        if teachingOrderAlgorithm == "elimination":
            # arrange the teaching order using the elimination algorithm
            #  N.B. this performs the function of StoreTeachingOrderBuildExampleWordsLists as well
            
            # make a copy of the graphemeUse dictionary, as we will be changing it
            graphemeUseCopy = self.graphemeUse.copy()
            # make a copy of the words dictionary, as we will be changing it
            wordsCopy = self.analysisWords.copy()
            # make a copy of the morphemes dictionary, as we will be changing it
            morphemesCopy = self.analysisMorphemes.copy()
            # start with an empty teaching order
            self.teachingOrder = []
            while len(graphemeUseCopy) > 0:
                # dict of { grapheme, sum of frequencies of all words that use this grapheme }
                currGraphemeFreq = {}
                for gr in graphemeUseCopy:
                    # find the sum of the frequencies of all the words having this grapheme
                    freq = 0
                    for morph in morphemesCopy:
                        # if this morpheme contains the grapheme, add it to the list
                        if gr in self.morphemesAsGraphemes[morph]:
                            # this morpheme contains the grapheme, add morpheme count (tokens) or just 1 if counting types
                            freq += morphemesCopy[morph] if countWords else 1
                    currGraphemeFreq[gr] = freq
                # find min value of currGraphemeFreq, introduce as last grapheme
                # (if there is more than one with same count, it will choose one "randomly")
                last = min(currGraphemeFreq, key=currGraphemeFreq.get)
                if graphemeUseCopy[last] > 0:
                    # only add to teaching order if it is counted
                    self.teachingOrder.insert(0, last)
                
                # build a dictionary of example words (with counts) that use this grapheme
                wordsWithGrapheme = {}
                for word in wordsCopy:
                    # if this word contains the grapheme, add it to the list
                    if last in self.wordsAsGraphemes[word]:
                        wordsWithGrapheme[word] = self.analysisWords[word]
                # delete all of the words found, so they are not used in calculations for more frequent graphemes
                # (those words are excluded because the infrequent grapheme it contains hasn't been introduced yet)
                for word in wordsWithGrapheme:
                    del wordsCopy[word]
                    # delete the morphemes from this word
                    affixList = self.words[word][kWordAffixForm].split(' ')
                    for morph in affixList:
                        morphNoHyphen = morph
                        if morphNoHyphen.endswith('-') or morphNoHyphen.startswith('-'):
                            # this is an affix, so remove the hyphen before splitting into graphemes
                            morphNoHyphen = morphNoHyphen.replace('-', '')
                        # this mopheme may have already been deleted in another word, so don't fail if it's not there
                        if morphNoHyphen in morphemesCopy:
                            del morphemesCopy[morphNoHyphen]
                # store the list of example words for this grapheme, in decreasing order of use
                self.graphemeExampleWords[last] = sorted(wordsWithGrapheme, key=wordsWithGrapheme.get, reverse=True)
                # remove this grapheme from the dictionary and repeat the process
                del graphemeUseCopy[last]
        else:
            # teachingOrderAlgorithm == "decreasing grapheme frequency"
            # sort the letters by order of decreasing occurance, as draft teaching order
            graphemeList = sorted(self.graphemeUse, key=self.graphemeUse.get, reverse=True)
            # store this teaching order and build lists of example words
            self.StoreTeachingOrderBuildExampleWordsLists(graphemeList)
        
        # reset flag for recording a change to the data
        self.teachingOrderChanged = False
    
    def StoreTeachingOrderBuildExampleWordsLists(self, graphemeList):
        '''Store the given list as the teaching order, starting with the last item
        of the list, and as graphemes are stored, build a list of words that use this grapheme.
        As words are used, they are removed from the word list, so they don't appear as example
        words any higher up in the teaching order.
        
        Parameter: graphemeList (list of str) - lines of text to be analyzed
        '''
        # make a copy of the words dictionary, as we will be changing it
        wordsCopy = self.analysisWords.copy()
        self.teachingOrder = []
        while len(graphemeList) > 0:
            # get the least frequent grapheme
            last = graphemeList.pop()
            self.teachingOrder.insert(0, last)
            # if this is a sight word lesson, don't need to do any of this
            if not isinstance(last, int):
                # build a dictionary of example words (with counts) that use this grapheme
                wordsWithGrapheme = {}
                for word in wordsCopy:
                    # if this word contains the grapheme, add it to the list
                    if last in self.wordsAsGraphemes[word]:
                        wordsWithGrapheme[word] = self.analysisWords[word]
                # delete all of the words found, so they are not used in calculations for more frequent graphemes
                # (those words are excluded because the infrequent grapheme it contains hasn't been introduced yet)
                for word in wordsWithGrapheme:
                    del wordsCopy[word]
                # store the list of example words for this grapheme, in decreasing order of use
                self.graphemeExampleWords[last] = sorted(wordsWithGrapheme, key=wordsWithGrapheme.get, reverse=True)
    
    def RunSightWordsDialog(self, sightWordList):
        '''Run a dialog to collect sight words.
        
        Parameter: sightWordList (list of str) - current list of words (or empty list)
        Return value: sight word list (could be empty list, or None if user clicked Cancel)
        '''
        global myGlobalWindow
        # run the SightWordsDialog until it is valid
        valid = False
        myGlobalWindow.theSightWordsDialog.SetSightWords(sightWordList)
        while not valid:
            if myGlobalWindow.theSightWordsDialog.Run():
                # user clicked OK in the SightWordsDialog dialog so collect list in entry field
                text = myGlobalWindow.theSightWordsDialog.GetSightWords()
                text = text.strip()
                text = text.lower()
                text = unicodedata.normalize('NFD', text)
                sightWordList = re.split(r'\s+', text)
                # assume we have a valid input
                valid = True
                if sightWordList == [''] or sightWordList == ['', '']:
                    # empty list is valid but make it really empty
                    sightWordList = []
                else:
                    # make sure they don't repeat using a set() trick
                    if len(sightWordList)!=len(set(sightWordList)):
                        # the elements in the list are not unique
                        valid = False
                if not valid:
                    # did not pass validity test, inform the user to correct the data
                    title = _("Error")
                    msg = _("All sight words must be separated by spaces, and must be unique.\n\nPlease try again.")
                    SimpleMessage(title, "dialog-error", msg)
            else:
                # user clicked cancel, which is valid, but we do nothing, just make sure list is None
                sightWordList = None
                valid = True
        myGlobalWindow.theSightWordsDialog.dialog.hide()
        
        # return the sight word list (could be empty)
        return sightWordList
    
    def InsertSightWordsInTeachingOrder(self, posn, wordList):
        '''Insert a sight word lesson at the given position in the teaching order,
        and attach the given list of sight words to the lesson.
        
        Parameter: posn (int) - index of the teaching order at which to insert the sight words lesson
                   wordList (list of str) - list of the sight words to add
        Return value: int with the index into the sightWords list
        '''
        # add this list of sight words at the end of the sightWords list (it is a list of lists)
        self.sightWords.append(wordList)
        # get index into the sightWords list and insert that in the teaching order
        swIdx = len(self.sightWords)
        self.teachingOrder.insert(posn, swIdx)
        return swIdx
    
    def RemoveSightWordsFromTeachingOrder(self, posn):
        '''Remove the sight word lesson at the given position in the teaching order.
        
        Parameter: posn (int) - index of the teaching order from which to remove a sight words lesson
        Return value: int with the index into the sightWords list
        '''
        # remove that sight word lesson from the teaching order
        swIdx = self.teachingOrder.pop(posn)
        # remove that list of sight words from the sightWords list
        self.sightWords.pop(swIdx-1)
        for i, letter in enumerate(self.teachingOrder):
            if isinstance(letter, int):
                if letter > swIdx:
                    # shift this index earlier
                    self.teachingOrder[i] -= 1
                    # adjust the lessonTexts dictionary
                    if letter in self.lessonTexts:
                        self.lessonTexts[letter-1] = self.lessonTexts[letter]
                        del self.lessonTexts[letter]
        return swIdx
    
    def TeachingOrderModified(self, listStore):
        '''The order of graphemes in the teaching order has been modified.
        (We arrive here following a drag-and-drop in the teaching order.)
        Build up the teaching order list from the ListStore, and recalculate
        the example words that are possible with this new order.
        
        Parameter: listStore - data storage for current teaching order
        '''
        # build up the graphemeList from the listStore
        graphemeList = []
        for row in listStore:
            graph = row[0]
            if graph[0] == '\u25CC':
                # character that has the dotted circle base prepended, delete that base
                graph = graph[1:]
            elif graph == '\u2686\u2686':
                # this is a sight word, find the sight word index from hidden fourth column
                graph = row[3]
            graphemeList.append(graph)
        
        # store this teaching order and build lists of example words
        self.StoreTeachingOrderBuildExampleWordsLists(graphemeList)
    
    def UpdateTeachingOrderList(self, listStore):
        '''Update the teaching order list in the listStore provided to reflect the
        current order proposed in the WordAnalysis object.
        
        Parameter: listStore - data storage for current teaching order
        '''
        # start by clearing the listStore
        listStore.clear()
        # if there isn't a teachingOrder yet, just return
        if not hasattr(self, 'teachingOrder'):
            return
        # add each element in the teaching order
        for letter in self.teachingOrder:
            if isinstance(letter, int):
                # this is a sight word entry, eyeballs for display letter
                dispLetter = '\u2686\u2686'
                cnt = ''
                # load list of words
                swIdx = letter
                words = self.sightWords[swIdx-1]
                # create a string from the list of words, separated by double spaces
                wordList = '  '.join(words)
            else:
                dispLetter = letter
                # if the first character is a combining diacritic
                if unicodedata.category(dispLetter[0]) == 'Mn':
                    # (previously test was if 0x0300 <= ord(dispLetter[0]) <= 0x036f)
                    # then prepend the dotted circle base character
                    dispLetter = '\u25CC' + dispLetter
                cnt = str(self.graphemeUse[letter])
                words = self.graphemeExampleWords[letter]
                # set sight word index as zero, so we can quickly know that this is not a sight word lesson
                swIdx = 0
                # make a list of words with the target letter highlighted in bold
                highlightedWords = []
                for word in words:
                    graphemes = self.wordsAsGraphemes[word]
                    highlightedGraphemes = [f"<b>{g}</b>" if g == letter else g for g in graphemes]
                    highlightedWords.append(''.join(highlightedGraphemes))
                # create a string from the list of words, separated by double spaces
                # put zero-width space in front, or markup may not appear
                wordList = '\u200B' + '  '.join(highlightedWords)
                
                # this is some dubugging code... using my main Chadian Arabic stories test data
                # the line for "k" is taller than it should be, but if we drag and drop to
                # another position in the list (with a change in cell text), then it usually
                # goes back to its proper height
                #if letter in ["k"]:
                    #logger.warning('{} example words: {}'.format(letter, wordList))
                    #wordList = "Testing: " + wordList
                    #wordList = wordList[100:300]
                #if letter in ["k", "u"]:
                    #logger.warning('{} example words: {}'.format(letter, wordList))
                    #wordList = wordList.replace("<b>", "")
                    #wordList = wordList.replace("</b>", "")
            
            ## this string could be real long, so truncate it
            ## earlier ListView had rendering problem, diacritics shift left!
            #if len(wordList) > 120:
                ## add ellipsis at the end of truncated string
                #wordList = wordList[0:120] + '\u2026'
            listStore.append([dispLetter, cnt, wordList, swIdx])
    
    def TeachingOrderDoubleClick(self, widget, row):
        '''User double-clicked on a lesson in the teaching order. If a letter,
        display a concordance of multi-word phrases that can be produced in the
        selected lesson. If a sight word lesson, edit the sight words.
        
        Parameters: widget, row - for accessing the active row in the TreeView
        '''
        global myGlobalWindow
        model = widget.get_model()
        # Get the letter for this row
        letter = model[row][0]
        if letter == "\u2686\u2686":
            # this is a sight word row, so offer to edit the sight words
            teachingOrderIdx = row.get_indices()[0]
            sightWordIdx = self.teachingOrder[teachingOrderIdx] - 1
            sightWordList = self.RunSightWordsDialog(self.sightWords[sightWordIdx])
            if sightWordList is not None:
                # user didn't click cancel
                if len(sightWordList) == 0:
                    # should we make sure that user wants to erase those sight words?
                    self.RemoveSightWordsFromTeachingOrder(teachingOrderIdx)
                    myGlobalWindow.teachingOrderListStore.remove(model.get_iter(row))
                else:
                    # just update the sightwords entry
                    self.sightWords[sightWordIdx] = sightWordList
                    model[row][2] = '  '.join(sightWordList)
        else:
            phrases = self.GetPhrases(row[0])
            if len(phrases) > 0:
                # only display a concordance if we have data
                # create and run a class instance of ConcordanceDialog
                myGlobalWindow.theConcordanceDialog.Run(letter, phrases)
            else:
                title = _("Information")
                msg = _("No phrases of two or more words available.")
                SimpleMessage(title, 'dialog-information', msg)
    
    def GetTeachingOrderText(self):
        '''Build a text version of the teaching order list.
        
        Return value: str of entire teaching order (formatted for text output)
        '''
        txt = ''
        # add each element in the teaching order
        for letter in self.teachingOrder:
            if isinstance(letter, int):
                # this is a sight word entry, eyeballs for display letter
                dispLetter = _("StWds")
                cnt = ''
                # load list of words
                words = self.sightWords[letter-1]
            else:
                dispLetter = letter
                # if the first character is a combining diacritic
                if unicodedata.category(dispLetter[0]) == 'Mn':
                    # (previously test was if 0x0300 <= ord(dispLetter[0]) <= 0x036f)
                    # then prepend the dotted circle base character
                    dispLetter = '\u25CC' + dispLetter
                cnt = str(self.graphemeUse[letter])
                words = self.graphemeExampleWords[letter]
            # make a list of words as a string
            wordList = '  '.join(words)
            txt += dispLetter+'\t'+ str(cnt)+'\t'+wordList+'\n'
        return txt
    
    def ReprocessTextsForChars(self):
        '''Reprocess all texts to find chars (e.g. if diacritics are now separated)
        '''
        # start with new character lists
        self.chars = {' ': 1, '\xa0': 1}
        self.wordBreakChars = [' ', '\xa0']  # must include space and no-break space
        self.wordFormChars = []
        # add all characters from the text data
        for lines in self.fileLines:
            #logger.debug('Reprocessing:', self.fileNames[i].encode('utf-8'), ' for chars')
            self.FindChars(lines)
    
    def ReprocessTextsForWords(self):
        '''Reprocess all texts to find words (e.g. given modified word break character information)
        '''
        # clear out current word data
        self.words = {}
        # find words in each file again
        for i in range(len(self.fileNames)):
            #logger.debug('Reprocessing:', self.fileNames[i].encode('utf-8'), ' for words')
            self.FindWords(self.fileLines[i])
    
    def ProcessAffixes(self):
        '''Words or affixes have changed. Make sure that all words in the word list have affixes marked appropriately.'''
        global myGlobalRenderer
        
        # create lists of prefixes and suffixes (by looking at position of '-' in affix list elements)
        prefixes = [a[:-1] for a in self.affixes if a.endswith('-')]
        suffixes = [a[1:] for a in self.affixes if a.startswith('-')]
        # sort affixes from longest to shortest (so mgba- will match before m-)
        prefixes.sort(key=len, reverse=True)
        suffixes.sort(key=len, reverse=True)
        #  create RegEx's for finding affixes 
        prefMatch = re.compile('^(' + '|'.join(a for a in prefixes) + ')')
        suffMatch = re.compile('(' + '|'.join(a for a in suffixes) + ')$')
        prefMarkupMatch = re.compile('^<b>(' + '|'.join(a for a in prefixes) + ')')
        suffMarkupMatch = re.compile('(' + '|'.join(a for a in suffixes) + ')</b>$')
        
        kWordCnt = 0
        kWordManual = 1
        kWordExclude = 2
        kWordAffixForm = 3
        kWordMarkupForm = 4
        
        zwj = ''
        if 'Scheherazade' in myGlobalRenderer.fontName or 'Harmattan' in myGlobalRenderer.fontName:
            # include zero width joiners (ZWJ, U+200D) for these two fonts, to approximate joining across markup
            zwj = '\u200d'
        
        # for each entry in the word list, see if there are any affixes to update
        for word, word_info in self.words.items():
            if not word_info[kWordManual] and not word_info[kWordExclude]:
                # this hasn't been marked up manually or excluded, so check to see if there are affixes to mark
                affix_word = word
                # process one each of any affixes
                if len(prefixes) > 0:
                    affix_word = prefMatch.sub('\\1- ', affix_word)
                if len(suffixes) > 0:
                    affix_word = suffMatch.sub(' -\\1', affix_word)
                word_info[kWordAffixForm] = affix_word
                
                markup_word = '<b>' + word + '</b>'
                # process one each of any affixes
                if len(prefixes) > 0:
                    markup_word = prefMarkupMatch.sub('<span foreground="gray">\\1'+zwj+'</span><b>'+zwj, markup_word)
                if len(suffixes) > 0:
                    markup_word = suffMarkupMatch.sub(zwj+'</b><span foreground="gray">'+zwj+'\\1</span>', markup_word)
                word_info[kWordMarkupForm] = markup_word
        
        # make sure we recalculate the teaching order when we display it (not dataChanged, correct?)
        self.teachingOrderChanged = True


    def RunAffixesDialog(self):
        '''Run a dialog to configure affixes in this language.
        
        Return value: True if the affix list changed, otherwise False
        '''
        global myGlobalWindow
        # save a copy of the list to compare later
        saveAffixes = self.affixes[:]
        # run the AffixesDialog until it is valid
        valid = False
        myGlobalWindow.theAffixesDialog.SetAffixes(self.affixes)
        while not valid:
            if myGlobalWindow.theAffixesDialog.Run():
                # user clicked OK in the Affixes dialog so collect list in textview field
                text = myGlobalWindow.theAffixesDialog.GetAffixes()
                text = text.strip()
                text = text.lower()
                text = unicodedata.normalize('NFD', text)
                affixList = re.split(r'\s+', text)
                # assume we have a valid input
                valid = True
                if affixList == [''] or affixList == ['', '']:
                    # empty list is valid but make it really empty
                    affixList = []
                    # save the list
                    self.affixes = affixList
                else:
                    # check each affix in list to make sure it is at least 2 chars, 
                    # and has '-' at beginning or end (but not both)
                    for affix in affixList:
                        if len(affix) < 2 or affix.count('-') != 1 or not (affix.startswith('-') ^ affix.endswith('-')):
                            # we have an invalid affix: too short, more than one '-', 
                            # or doesn't start or end with '-' (but not both - XOR)
                            valid = False
                            break
                    # make sure they don't repeat using a set() trick
                    if len(affixList) != len(set(affixList)):
                        # the elements in the list are not unique
                        valid = False
                    if valid:
                        # passed validity test, so save the list
                        self.affixes = affixList
                    else:
                        # did not pass validity test, inform the user to correct the data
                        title = _("Error")
                        msg = _("All affixes must start or end with '-',\nmust be separated by spaces, and must be unique.\n\nPlease try again.")
                        SimpleMessage(title, "dialog-error", msg)
            else:
                # user clicked cancel, which is valid, but we do nothing
                valid = True
        myGlobalWindow.theAffixesDialog.dialog.hide()
        # return True if the list changed
        return (self.affixes != saveAffixes)
    
    def RunWordBreaksDialog(self):
        '''Run a dialog which configures word break characters in this language.
        
        Return value: True if the character list changed, otherwise False
        '''
        global myGlobalWindow
        # save a copy of the list to compare later
        saveChars = self.wordBreakChars[:]
        # run the WordBreaksDialog
        if myGlobalWindow.theWordBreaksDialog.Run(self.wordBreakChars, self.wordFormChars):
            # user clicked OK, so get and store data from the listStores
            # make sure to include the invisible space and invisible non-breaking space
            self.wordBreakChars = [' ', '\xa0'] + myGlobalWindow.theWordBreaksDialog.GetWordBreakChars()
            self.wordFormChars = myGlobalWindow.theWordBreaksDialog.GetWordFormChars()
        # return True if the list changed
        return (sorted(self.wordBreakChars) != sorted(saveChars))
    
    def RunDigraphsDialog(self):
        '''Run a dialog to configure digraphs in this language.
        
        Return value: True if the digraph list changed, otherwise False
        '''
        global myGlobalWindow
        # save a copy of the list to compare later
        saveDigraphs = self.digraphs[:]
        # run the DigraphsDialog until it is valid
        valid = False
        myGlobalWindow.theDigraphsDialog.SetDigraphs(self.digraphs)
        while not valid:
            # run the digraphs dialog
            if myGlobalWindow.theDigraphsDialog.Run():
                # user clicked OK in the Digraphs dialog so collect list in textview field
                text = myGlobalWindow.theDigraphsDialog.GetDigraphs()
                text = text.strip()
                text = text.lower()
                text = unicodedata.normalize('NFD', text)
                digraphList = re.split(r'\s+', text)
                # assume we have a valid input
                valid = True
                if digraphList == [''] or digraphList == ['', '']:
                    # empty list is valid but make it really empty
                    digraphList = []
                else:
                    # check each digraph in list to make sure it is at least 2 chars
                    for digraph in digraphList:
                        if len(digraph) < 2:
                            # we have an invalid digraph
                            valid = False
                            break
                    # make sure they don't repeat using a set() trick
                    if len(digraphList) != len(set(digraphList)):
                        # the elements in the list are not unique
                        valid = False
                if valid:
                    # passed validity test, so save the list
                    self.digraphs = digraphList
                else:
                    # did not pass validity test, inform the user to correct the data
                    title = _("Error")
                    msg = _("All digraphs must have at least two characters,\nmust be separated by spaces, and must be unique.\n\nPlease try again.")
                    SimpleMessage(title, 'dialog-error', msg)
            else:
                # user clicked cancel, which is valid, but we do nothing
                valid = True
        myGlobalWindow.theDigraphsDialog.dialog.hide()
        
        # if the list changed, make sure we recalculate the teaching order when we display it
        if (self.digraphs != saveDigraphs):
            self.dataChanged = True
            self.teachingOrderChanged = True
    
    def RunWordEditDialog(self, widget, row):
        '''Ask user to edit the affix breaks, show a concordance of the selected word.
        
        Parameters: widget, row - for accessing the active row in the TreeView
        '''
        global myGlobalRenderer
        global myGlobalWindow
        model = widget.get_model()
        # get the word for this row, both markup and plain (from hidden column) forms
        markup_word = model[row][0]
        word = model[row][2]
        
        kWordCnt = 0
        kWordManual = 1
        kWordExclude = 2
        kWordAffixForm = 3
        kWordMarkupForm = 4
        
        #  get the word info, which is modifiable (in place)
        word_info = self.words[word]
        
        #  get a concordance of this word
        concordance = self.GetConcordance(word)
        
        zwj = ''
        if 'Scheherazade' in myGlobalRenderer.fontName or 'Harmattan' in myGlobalRenderer.fontName:
            # include zero width joiners (ZWJ, U+200D) for these two bad fonts, to approximate joining across markup
            zwj = '\u200d'
        
        
        valid = False
        while not valid:
            # run the word edit dialog
            if myGlobalWindow.theWordEditDialog.Run(word, word_info[kWordAffixForm], word_info[kWordExclude], concordance):
                # user clicked OK in the WordEditDialog, assume we have a valid input
                valid = True
                # check if we should exclude it
                if myGlobalWindow.theWordEditDialog.excludeWord.get_active():
                    # mark word as excluded
                    word_info[kWordExclude] = True
                    # make excluded word all gray, and save empty string in specialWordSplits
                    markup_word = '<span foreground="gray">' + word + '</span>'
                    word_info[kWordMarkupForm] = markup_word
                    markup_word = '\u200B' + markup_word
                    # can't use model[row][0] = markup_word, because TreeModelSort has no attribute set_value
                    # so we have to go indirectly through the child filterModel, using a converted iter
                    childFilterModel = model.get_model()
                    childIter = model.convert_iter_to_child_iter(model.get_iter(row))
                    childFilterModel[childIter][0] = markup_word
                    word_info[kWordAffixForm] = word
                    
                    # make sure we recalculate the teaching order when we display it
                    self.dataChanged = True
                    self.teachingOrderChanged = True
                else:
                    # collect text in entry field
                    text = myGlobalWindow.theWordEditDialog.divideBuffer.get_text(
                        myGlobalWindow.theWordEditDialog.divideBuffer.get_start_iter(),
                        myGlobalWindow.theWordEditDialog.divideBuffer.get_end_iter(), False)
                    text = text.strip()
                    text = text.lower()
                    text = unicodedata.normalize('NFD', text)
                    morphemeList = re.split(r'\s+', text)
                    if morphemeList == [''] or morphemeList == ['', '']:
                        # empty list is not valid in this context
                        valid = False
                        # inform the user to correct the data
                        title = _("Error")
                        msg = _("An empty division of the word is not allowed.\n\nPlease try again.")
                        SimpleMessage(title, "dialog-error", msg)
                    else:
                        # make a rejoined form, without hyphens
                        rejoined = ''.join(morphemeList).replace('-', '')
                        ratio = self.LevenshteinRatio(word, rejoined)
                        if ratio < 0.5:
                            # the Levenshtein ratio is quite low - really the same word?
                            title = _("Significant Change")
                            msg = _("""Your word division '{}' reflects a very different word form
than the original word '{}'. Are you sure it is correct?""").format(' '.join(morphemeList), word)
                            if not SimpleYNQuestion(title, 'dialog-warning', msg):
                                valid = False
                                continue
                        # check each morpheme in list to make sure it is valid
                        # at this point requires all prefixes first, then roots, then suffixes
                        stage = 'prefix'
                        numroots = 0
                        for morpheme in morphemeList:
                            if stage == 'prefix':
                                if morpheme.endswith('-'):
                                    # stay in prefix stage
                                    if len(morpheme) < 2 or morpheme.count('-') != 1:
                                        # invalid morpheme: too short, or too many hyphens
                                        valid = False
                                        break
                                else:
                                    #  move to root stage
                                    stage = 'root'
                            if stage == 'root':
                                if morpheme.startswith('-'):
                                    #  move to suffix stage
                                    stage = 'suffix'
                                else:
                                    numroots += 1
                                    if morpheme.endswith('-') or morpheme.count('-') > 1:
                                        # invalid morpheme: marked as prefix, or too many hyphens
                                        valid = False
                                        break
                            if stage == 'suffix':
                                if not morpheme.startswith('-') or morpheme.count('-') != 1:
                                    # invalid morpheme: not marked as suffix, or too many hyphens
                                    valid = False
                                    break
                        
                        if numroots < 1:
                            # not enough roots
                            valid = False
                        
                        if valid:
                            # valid entry built from text field
                            # word is not excluded
                            word_info[kWordExclude] = False
                            # store affix form
                            affix_word = ' '.join(morphemeList)
                            word_info[kWordAffixForm] = affix_word
                            # remember that this is a manually modified form
                            word_info[kWordManual] = True
                            # change all affixes in morphemeList into gray <span> forms
                            # and put <b></b> around roots
                            markup_word = ''
                            for m in morphemeList:
                                if m.endswith('-'):
                                    markup_word += '<span foreground="gray">' + m.replace('-', '') + '</span>'
                                elif m.startswith('-'):
                                    markup_word += '<span foreground="gray">' + m.replace('-', '') + '</span>'
                                else:
                                    markup_word += '<b>' + m + '</b>'
                            # remove </b><b> pairs in the middle (will happen if there are 2+ roots)
                            markup_word = markup_word.replace('</b><b>', '')
                            if zwj:
                                # include zero width joiners (ZWJ, U+200D) at transitions if we are using a bad font
                                markup_word = re.sub('(</span>|</b>)(<span foreground="gray">|<b>)', '\u200d\\1\\2\u200d', markup_word)
                            
                            word_info[kWordMarkupForm] = markup_word
                            # put zero-width space in front, or markup may not appear
                            markup_word = '\u200B' + markup_word
                            # can't use model[row][0] = markup_word, because TreeModelSort has no attribute set_value
                            # so we have to go indirectly through the child filterModel, using a converted iter
                            childFilterModel = model.get_model()
                            childIter = model.convert_iter_to_child_iter(model.get_iter(row))
                            childFilterModel[childIter][0] = markup_word
                            
                            # make sure we recalculate the teaching order when we display it
                            self.dataChanged = True
                            self.teachingOrderChanged = True
                        else:
                            # did not pass validity test, inform the user to correct the data
                            title = _("Invalid entry")
                            msg = _("""All prefixes must end with '-', all suffixes must begin with '-',
there must be at least one root without '-', all must be separated by spaces.

Please try again.""")
                            SimpleMessage(title, "dialog-error", msg)
            else:
                # user clicked cancel, which is valid, but we do nothing
                valid = True
        myGlobalWindow.theWordEditDialog.dialog.hide()
    
    def GetConcordance(self, word):
        '''Return a string which contains a concordance of the given word in context.
        Each line of the concordance looks like this:
           pre-context \t word \t post-context \n
        
        Parameter: word (str) - the word to find in the text
        Return value: (str) - "concordance" of word in context
        '''
        # build 'breaks' string with all word breaking characters for RegEx matching
        breaks = ' '
        for char in self.wordBreakChars:
            # need to put '\' before special characters
            if char in '.^$*+-?{}\\[]|()':
                breaks = breaks + '\\'
            breaks = breaks + char
        
        concordance = ""
        for fileNum in range(len(self.fileNames)):
            for line in self.fileLines[fileNum]:
                # we split the line, which returns a list of strings with
                # the word desired (as elements 1,3,...)
                # and with the surrounding context (as elements 0,2,4,...)
                wordsFound = re.split("("+word+")", line, 0, re.I)
                # for i = each odd index in the list (ie. index of each word found)
                for i in range(1, len(wordsFound), 2):
                    pretext = "".join(wordsFound[:i])
                    # skip if the word is not immediately preceded by word break char
                    if len(pretext)>0 and pretext[-1] not in breaks:
                        continue
                    posttext = "".join(wordsFound[i+1:])
                    # skip if the word is not immediately followed by word break char
                    if len(posttext)>0 and posttext[0] not in breaks:
                        continue
                    # limit the context to 40 characters before/after
                    if len(pretext)>40: pretext = pretext[-40:]
                    if len(posttext)>40: posttext = posttext[:40]
                    # only show full words in the pretext and posttext
                    m = re.search(r'[\s' + breaks + ']+(.+)', pretext)
                    if m:
                        # only keep the text found after the first breaks
                        pretext = m.group(1)
                    m = re.search(r'(.+[\s' + breaks + ']+)', posttext)
                    if m:
                        # only keep the text up to and including last breaks
                        posttext = m.group(1)
                    # store this information as a line in the concordance
                    # make sure to remove any tab characters in strings, to not throw off columns
                    concordance += pretext.replace('\t', ' ') + "\t" + \
                                   wordsFound[i].replace('\t', ' ') + "\t" + \
                                   posttext.replace('\t', ' ') + "\n"
        # return the concordance, but without the final newline
        return concordance[:-1]
    
    def GetPhrases(self, row):
        '''Return a string which contains a "concordance" of the phrases that are
        possible by using the words that are available at this row number and
        higher in the teaching order. Each line of the concordance looks like this:
           pre-context \t phrase \t post-context \n
        
        Parameter: row (int) - include letters/words down to this row number
                               from the teaching order
        Return value: (str) - "concordance" of phrases possible with these letters
        '''
        # build 'breaks' string with a list of all of the word-breaking
        # characters for RegEx matching
        breaks = ''
        for char in self.wordBreakChars:
            # need to put '\' before special characters
            if char in '.^$*+-?{}\\[]|()':
                breaks = breaks + '\\'
            breaks = breaks + char
        
        # build up a list of all possible words using letters that are
        # taught down to row #row
        possibleWords = []
        for i in range(row+1):
            letter = self.teachingOrder[i]
            if isinstance(letter, int):
                # add sight word list
                possibleWords.extend(self.sightWords[letter-1])
            else:
                # add example word list
                possibleWords.extend(self.graphemeExampleWords[letter])
        
        # build a list of tuples that contain the length of the found string
        # (because we want to put the longest strings first)
        phraseList = []
        for fileNum in range(len(self.fileNames)):
            for line in self.fileLines[fileNum]:
                # turn tabs in text into spaces (since tabs delineate the concordance)
                line = line.replace('\t', ' ')
                # split the line into words
                linewords = re.split(r'([\s' + breaks + r']+)', line)
                i = 0
                while i < len(linewords):
                    if linewords[i].lower() in possibleWords:
                        j = i+2
                        while j < len(linewords) and \
                              linewords[j].lower()in possibleWords:
                            j += 2
                        if j > i+2:
                            # we have at least 2 example words together
                            strt = max(i-6, 0) # try to show 3 words before as context
                            fnsh = min(j+6, len(linewords)) # and 3 words after
                            phrase = ''.join(linewords[strt:i]) + "\t"
                            possiblePhrase = ''.join(linewords[i:j-1])
                            phrase += possiblePhrase + "\t"
                            phrase += ''.join(linewords[j-1:fnsh]) + "\n"
                            # add this phrase to the list, with the length of its possible phrase
                            phraseList.append( (len(possiblePhrase), phrase) )
                            # move counter past last example word already matched
                            i = j
                    i += 1
        # combine the phrases, longest possible phrase first
        phrases = ""
        for (ln, s) in sorted(phraseList, reverse=True):
            phrases += s
        # return the phrases, but without the final newline
        return phrases[:-1]
    
    def LevenshteinRatio(self, s, t):
        ''' Calculates levenshtein distance ratio of similarity between two strings.
            For all i and j, distance[i,j] will contain the Levenshtein
            distance between the first i characters of s and the
            first j characters of t
        '''
        # Initialize matrix of zeros
        rows = len(s)+1
        cols = len(t)+1
        distance = np.zeros((rows,cols),dtype = int)
        
        # Populate matrix of zeros with the indices of each character of both strings
        for i in range(1, rows):
            for k in range(1,cols):
                distance[i][0] = i
                distance[0][k] = k
        
        # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions    
        for col in range(1, cols):
            for row in range(1, rows):
                if s[row-1] == t[col-1]:
                    # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
                    cost = 0
                else:
                    # Since we're calculating ratio, the cost of a substitution is 2 (to align with results of the Python Levenshtein package)
                    cost = 2
                distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                     distance[row][col-1] + 1,          # Cost of insertions
                                     distance[row-1][col-1] + cost)     # Cost of substitutions
        
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    
    
    def __init__(self):
        '''Initialize this WordAnalysis object.
        '''
        # fileNames: list of file names (with path) that have been loaded
        self.fileNames = []
        # fileLines: list of lists of lines in the files
        self.fileLines = []
        # note that fileLines[n] is a list of lines in fileNames[n]
        
        # flag for if the data contains NFC composed characters
        self.containsNFC = False
        # flag for if the data contains NFD decomposed characters
        self.containsNFD = False
        # flag for if the user has been warned about inconsistent encoding
        self.userInformedEncodingError = False
        
        # chars: dictionary of { char: 1 } for all characters used in all texts
        self.chars = {' ': 1, '\xa0': 1}
        # lists of characters that are used for word breaking or word forming
        self.wordBreakChars = [' ', '\xa0']  # must include space and no-break space
        self.wordFormChars = []
        # digraphs: list of character combinations that should be considered digraphs
        self.digraphs = []
        # affixes: list of affixes, each of which includes '-' at beginning or end, to indicate attach point
        self.affixes = []
        # specialWordSplits: dict of { word, string of the word with broken off affixes (overrides use of affix list) }
        self.specialWordSplits = {}
        
        # words: dict of { word, [word count in all texts, manual split?, excluded?, affix form, markup form] }
        self.words = {}
        
        # lessonTexts: dict of { grapheme (str), text of that lesson (str) }
        #    note: the grapheme can alternately be an integer which is an index into the sight word list
        self.lessonTexts = {}
        self.selectedGrapheme = None
        
        # default value for treating combining diacritics separately
        self.separateCombDiacritics = False
        # define default parameters for dealing with SFM files
        self.sfmProcessSFMs = False
        self.sfmIgnoreLines = 'id|rem|restore|h|toc1|toc2|toc3'
        self.sfmProcessLines = ''
        
        # flag for if the data changed
        self.dataChanged = False
        # flag for if the Teaching Order needs to be rebuilt (similar but not identical to the above)
        self.teachingOrderChanged = False



class GtkBuilder(Gtk.Builder):

    def __init__(self, glade_file, APP_NAME):
        super().__init__()
        self.set_translation_domain(APP_NAME)
        self.add_from_file(glade_file)

        self.tree = ET.parse(glade_file)
        self.recursive_xml_translate(self.tree.getroot())

    def recursive_xml_translate(self, node):
        '''Custom translation with Glade/Builder does not work when locale is not installed.
        Reset every label in Glade file using gettext.'''
        def func_not_found(value):
            logger.warning('could not translate: {}'.format(value))
        
        parent_id = node.attrib.get('id')

        for child in node:
            if len(child):
                self.recursive_xml_translate(child)

            if not child.attrib.get('translatable') == 'yes':
                continue

            # translate property value
            if child.tag == 'property' and parent_id and child.attrib.get('name'):
                name = child.attrib.get('name')
                obj = self.get_object(parent_id)
                func = getattr(obj, 'set_{}'.format(name), func_not_found)
                translatedString = _(child.text)
                #logger.debug('Translate Glade object ({}): set_{}({})'.format(
                    #parent_id, name, translatedString ))
                func(_(translatedString))


class Handler:
    def on_mainWindow_delete_event(self, *args):
        self.quit_confirmation_dialog()
        # if we returned, then we shouldn't quit
        return True
    
    def on_quitMenuItem_activate(self, *args):
        self.quit_confirmation_dialog()
    
    def quit_confirmation_dialog(self):
        global myGlobalWindow
        if myGlobalWindow.analysis.dataChanged:
            # confirm overwriting it
            title = _("Confirm quit")
            msg = _("There is unsaved data. Quit anyway?")
            if not SimpleYNQuestion(title, 'dialog-warning', msg):
                # no, we shouldn't quit
                return
        # either data hasn't changed since last save or user confirmed to quit anyway
        Gtk.main_quit()
    
    def on_newProjectMenuItem_activate(self, *args):
        global myGlobalWindow
        myGlobalWindow.NewProject()
    
    def on_openProjectMenuItem_activate(self, *args):
        global myGlobalWindow
        myGlobalWindow.OpenProject()
    
    def on_saveProjectMenuItem_activate(self, *args):
        global myGlobalWindow
        myGlobalWindow.SaveProject()
    
    def on_saveProjectAsMenuItem_activate(self, *args):
        global myGlobalWindow
        myGlobalWindow.SaveProjectAs()
    
    def on_saveTeachingOrderMenuItem_activate(self, *args):
        '''Process the File > Save Teaching Order menu.'''
        global myGlobalWindow
        global myGlobalPath
        msg = _("Save teaching order as...")
        chooser = Gtk.FileChooserDialog(title=msg, parent=myGlobalWindow.window,
                                        action=Gtk.FileChooserAction.SAVE)
        chooser.add_buttons(Gtk.STOCK_SAVE, Gtk.ResponseType.OK,
                            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        chooser.set_transient_for(myGlobalWindow.window)
        chooser.set_current_name(_("TeachingOrder.txt"))
        chooser.set_current_folder(myGlobalPath)
        chooser.set_do_overwrite_confirmation(True)
        chooser.set_default_response(Gtk.ResponseType.OK)
        if chooser.run() == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            filetext = myGlobalWindow.analysis.GetTeachingOrderText()
            # write out the data
            myGlobalWindow.WriteFile(filename, filetext, myGlobalWindow.analysis.containsNFC, myGlobalWindow.analysis.containsNFD)
            # save this path for next time we need to write out a file
            myGlobalPath = os.path.dirname(filename)
        chooser.destroy()
    
    def on_saveWordListMenuItem_activate(self, *args):
        '''Process the File > Save Teaching Order menu.'''
        global myGlobalWindow
        global myGlobalPath
        msg = _("Save word list as...")
        chooser = Gtk.FileChooserDialog(title=msg, parent=myGlobalWindow.window,
                                        action=Gtk.FileChooserAction.SAVE)
        chooser.add_buttons(Gtk.STOCK_SAVE, Gtk.ResponseType.OK,
                            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        chooser.set_transient_for(myGlobalWindow.window)
        chooser.set_current_name(_("WordList.txt"))
        chooser.set_current_folder(myGlobalPath)
        chooser.set_do_overwrite_confirmation(True)
        chooser.set_default_response(Gtk.ResponseType.OK)
        if chooser.run() == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            filetext = ''
            kWordCnt = 0
            kWordManual = 1
            kWordExclude = 2
            kWordAffixForm = 3
            kWordMarkupForm = 4
            
            # save the higher frequency words first
            for word in sorted(myGlobalWindow.analysis.words, key=myGlobalWindow.analysis.words.get, reverse=True):
                word_info = myGlobalWindow.analysis.words[word]
                if len(myGlobalWindow.analysis.affixes) == 0:
                    # no affixes, just print out word and count
                    filetext = filetext + word + '\t' + str(word_info[kWordCnt]) + '\n'
                else:
                    #  print out word, count, and affix form
                    filetext = filetext + word + '\t' + str(word_info[kWordCnt]) + '\t' + word_info[kWordAffixForm] + '\n'
            # write out the data
            myGlobalWindow.WriteFile(filename, filetext, myGlobalWindow.analysis.containsNFC, myGlobalWindow.analysis.containsNFD)
            # save this path for next time we need to write out a file
            myGlobalPath = os.path.dirname(filename)
        chooser.destroy()
    
    def on_selectFontMenuItem_activate(self, *args):
        '''Process the Configure > Select the Text Font menu, to choose display font.'''
        global myGlobalWindow
        global myGlobalRenderer
        if myGlobalRenderer.SelectFont():
            myGlobalWindow.ApplyNewFont()
    
    def on_interfaceMenuItem_activate(self, widget, lang, idx):
        global myGlobalWindow
        global myGlobalBuilder
        global myGlobalConfig
        global _
        settings = myGlobalWindow.window.get_settings()
        fontname = translation_languages[idx][2]
        if len(fontname) == 0:
            # set font based on OS
            if platform.system() == "Windows":
                fontname = 'Segoe UI 12'
            else:
                fontname = 'Ubuntu 12'
        settings.set_property('gtk-font-name', fontname)
        if translation_languages[idx][3] == 'RTL':
            myGlobalWindow.window.set_default_direction(Gtk.TextDirection.RTL)
            myGlobalWindow.isRTL = True
            #myGlobalBuilder.get_object('teachingOrderScrolledWindow').get_hadjustment().set_value(100)
        else:
            myGlobalWindow.window.set_default_direction(Gtk.TextDirection.LTR)
            myGlobalWindow.isRTL = False
            #myGlobalBuilder.get_object('teachingOrderScrolledWindow').get_hadjustment().set_value(0)
        _ = translation_languages[idx][4].gettext
        myGlobalBuilder.recursive_xml_translate(myGlobalBuilder.tree.getroot())
        # this will make the affixes list empty, so update the list
        myGlobalWindow.UpdateAffixList()
        myGlobalWindow.ShowSummaryStatusBar()
        
        # update config object and save
        myGlobalConfig['Option']['lang'] = lang
        SaveConfig()
    
    def on_helpMenuItem_activate(self, *args):
        '''Process the Help > PrimerPrep Help menu. Display help web page.'''
        global myGlobalConfig
        global myGlobalProgramPath
        
        lang = myGlobalConfig['Option']['lang']
        filename = os.path.join(myGlobalProgramPath, 'Help', "PrimerPrepHelp-" + lang + ".htm")
        if not os.path.exists(filename):
            title = _("Warning")
            msg = _("The help file was not found.")
            SimpleMessage(title, "dialog-warning", msg)
        else:
            webbrowser.open("file:///" + filename)
    
    def on_feedbackMenuItem_activate(self, *args):
        '''Process the Help > Give Feedback menu. Go to Google form web page.'''
        #global myGlobalConfig
        #lang = myGlobalConfig['Option']['lang']'   # May eventually want to go to a different page dependent on UI language?
        webbrowser.open("https://docs.google.com/forms/d/e/1FAIpQLSddxvDvbn0uohOt7J4Gcc48KgLxg1q4hOfjeYLRSUlKB4pQUw/viewform?usp=sf_link", new=2)
    
    def on_aboutMenuItem_activate(self, *args):
        '''Process the Help > About menu. Display information about the program.'''
        title = _("About")
        msg = "PrimerPrep version " + progVersion
        msg += "\n" + _("Developed by Jeff Heath, SIL Chad") + "\n\n"
        msg += "© " + progYear + " SIL Global\n\n"
        msg += _("""This is a tool that helps in preparing a primer.
The program loads language texts, counts words
and letters, and suggests a teaching order for
introducing the letters in a primer.""")
        SimpleMessage(title, "dialog-information", msg)
    
    def on_addTextsButton_clicked(self, *args):
        '''Using a FileChooserDialog, allow user to select and open file(s) for analysis.'''
        global myGlobalWindow
        # run the open file dialog, and handle loading any file(s) chosen
        myGlobalWindow.AddTexts()
    
    def on_chooseLexiconButton_clicked(self, *args):
        '''Using a FileChooserDialog, allow user to select and open a lexicon file
        (LIFT or SFM format file).
        '''
        title = _("Information")
        msg = _("Feature coming soon!")
        SimpleMessage(title, 'dialog-information', msg)
        
    def on_showFullPathCheckButton_toggled(self, *args):
        global myGlobalBuilder
        global myGlobalWindow
        fileListStore = myGlobalBuilder.get_object('fileListStore')
        fileListStore.clear()
        for filename in myGlobalWindow.analysis.fileNames:
            if myGlobalBuilder.get_object('showFullPathCheckButton').get_active():
                name = filename
            else:
                name = filename.split('\\')[-1]
            fileListStore.append([name])
    
    def on_affixesRadioButton_toggled(self, *args):
        global myGlobalWindow
        global myGlobalConfig
        global myGlobalBuilder
        # make sure we recalculate the teaching order next time we display it
        myGlobalWindow.analysis.dataChanged = True
        myGlobalWindow.analysis.teachingOrderChanged = True
        # update config object and save
        myGlobalConfig['Option']['excludeaffixes'] = '1' if myGlobalBuilder.get_object('affixesExcludedRadioButton').get_active() else '0'
        SaveConfig()
    
    def on_editAffixesButton_clicked(self, button):
        '''Allow the user to define prefixes and suffixes that should be broken off in words.'''
        global myGlobalWindow
        # just pass this job to the analysis object
        if myGlobalWindow.analysis.RunAffixesDialog():
            # returned True, so the affix list changed - recalculate data
            title = _("Reprocessing texts")
            msg = _("The list of affixes changed, so all of the\ntext data is being reprocessed.")
            SimpleMessage(title, "dialog-warning", msg)
            
            myGlobalWindow.UpdateAffixList()
            myGlobalWindow.analysis.ProcessAffixes()
            myGlobalWindow.analysis.UpdateWordList(myGlobalWindow.wordListStore)
            myGlobalWindow.analysis.dataChanged = True
    
    def on_countWordRadioButton_toggled(self, *args):
        global myGlobalWindow
        global myGlobalConfig
        global myGlobalBuilder
        # make sure we recalculate the teaching order next time we display it
        myGlobalWindow.analysis.dataChanged = True
        myGlobalWindow.analysis.teachingOrderChanged = True
        # update config object and save
        myGlobalConfig['Option']['countallwords'] = '1' if myGlobalBuilder.get_object('countWordEachTimeRadioButton').get_active() else '0'
        SaveConfig()
        
    def on_wordBreakingCharsButton_clicked(self, button):
        global myGlobalWindow
        # just pass this job to the analysis object
        if myGlobalWindow.analysis.RunWordBreaksDialog():
            # returned True, so word break char list changed - reprocess all texts
            title = _("Reprocessing texts")
            msg = _("The list of word-breaking characters changed, so all\nof the text data is being reprocessed.")
            SimpleMessage(title, "dialog-warning", msg)
            # ask the WordAnalysis object to reprocess all texts again
            myGlobalWindow.analysis.ReprocessTextsForWords()
            # display the updated results
            myGlobalWindow.analysis.UpdateWordList(myGlobalWindow.wordListStore)
            myGlobalWindow.analysis.dataChanged = True
            myGlobalWindow.ShowSummaryStatusBar()
    
    def on_digraphsButton_clicked(self, button):
        '''Allow the user to define digraphs that should be identified in the language.'''
        global myGlobalWindow
        # just pass this job to the analysis object, will set dataChanged, if appropriate
        myGlobalWindow.analysis.RunDigraphsDialog()
    
    def on_separateDiacriticsCheckButton_toggled(self, widget, data=None):
        global myGlobalWindow
        global myGlobalConfig
        # menu processing has already toggled checkmark, we just load in its value
        myGlobalWindow.analysis.separateCombDiacritics = widget.get_active()
        # update config object and save
        myGlobalConfig['Option']['separatecombdia'] = '1' if widget.get_active() else '0'
        SaveConfig()
        
        # make sure that we recalculate the teaching order
        myGlobalWindow.analysis.dataChanged = True
        myGlobalWindow.analysis.teachingOrderChanged = True
        
        # rebuild the character lists, since they could be different now
        myGlobalWindow.analysis.ReprocessTextsForChars()
    
    def on_filterTextEntry_changed(self, widget):
        global myGlobalBuilder
        global myGlobalWindow
        wordListTreeModelFilter = myGlobalBuilder.get_object("wordListTreeModelFilter")
        wordListTreeModelFilter.refilter()
        myGlobalWindow.ShowSummaryStatusBar()

    def on_wordListTreeView_row_activated(self, widget, row, col):
        global myGlobalWindow
        # just pass this job to the analysis object, will set dataChanged, if appropriate
        myGlobalWindow.analysis.RunWordEditDialog(widget, row)
    
    def on_addSightWordsButton_clicked(self, button):
        '''Add a line for sight words in the teaching order, entered by user.'''
        global myGlobalWindow
        if len(myGlobalWindow.teachingOrderListStore) == 0:
            # no teaching order, just exit quietly
            return
        (model, row) = myGlobalWindow.teachingOrderTreeView.get_selection().get_selected()
        if row is None:
            # no line selected, just exit quietly
            return
        # just pass the job of collecting the sight word list to the analysis object
        sightWordList = myGlobalWindow.analysis.RunSightWordsDialog([])
        if sightWordList is not None and len(sightWordList) > 0:
            # there are sight words to add, start at selected row
            # get path and index of selected row
            path = model.get_path(row)
            idx = path.get_indices()[0]
            swIdx = myGlobalWindow.analysis.InsertSightWordsInTeachingOrder(idx, sightWordList)
            # add the sight word lesson in the ListStore
            myGlobalWindow.teachingOrderListStore.insert(idx, ['\u2686\u2686', '', '  '.join(sightWordList), swIdx])
            # select equivalent row in teaching order
            myGlobalWindow.teachingOrderTreeView.get_selection().select_path(path)
            myGlobalWindow.analysis.dataChanged = True
    
    def on_removeSightWordsButton_clicked(self, button):
        '''Remove a line of sight words from the teaching order.'''
        global myGlobalWindow
        # find the selected row (the sight word lesson to remove)
        (model, row) = myGlobalWindow.teachingOrderTreeView.get_selection().get_selected()
        if row is not None:
            # get the sight word index, tucked away in the hidden column
            swIdx = myGlobalWindow.teachingOrderListStore.get_value(row, 3)
            if swIdx > 0:
                # this is a sight word lesson, so remove it
                # get path and index of selected row
                path = model.get_path(row)
                idx = path.get_indices()[0]
                if swIdx != myGlobalWindow.analysis.RemoveSightWordsFromTeachingOrder(idx):
                    logger.error("Non-matching swIdx in on_removeSightWordsButton_clicked")
                # invalidate the selected grapheme, to make sure that any existing lesson text doesn't get re-saved somewhere
                # (the following ListStore.remove causes the on_Lesson_select routine to be called)
                myGlobalWindow.analysis.selectedGrapheme = None
                # remove the sight word lesson from the ListStore
                myGlobalWindow.teachingOrderListStore.remove(row)
                # adjust the fourth (hidden) column for sight word indices greater than the one deleted
                for rw in myGlobalWindow.teachingOrderListStore:
                    if rw[3] > swIdx:
                        rw[3] -= 1
                myGlobalWindow.analysis.dataChanged = True
            else:
                logger.error("Tried to remove a sight word lesson that was not a sight word lesson")
    
    def on_teachingOrderTreeView_row_activated(self, widget, row, col):
        '''Double-click on a row, just pass this job to the analysis object.
        It will display concordance for a letter, or edit a sight word lesson.
        '''
        global myGlobalWindow
        myGlobalWindow.analysis.TeachingOrderDoubleClick(widget, row)
    
    def on_teachingOrderTreeView_drag_begin(self, treeview, drag_context):
        global myGlobalWindow
        treeselection = treeview.get_selection()
        model, iter = treeselection.get_selected()
        myGlobalWindow.letterDragged = model.get_value(iter, 0)
        
    def on_teachingOrderTreeView_drag_end(self, treeview, context):
        '''Process the drag-and-drop which just ended. The teaching order has
        changed, so we need to store the new teaching order and recalculate
        the example words that are possible with this new order.
        
        Parameters: treeview (unused)
                    context (unused)
        '''
        global myGlobalWindow
        myGlobalWindow.analysis.TeachingOrderModified(myGlobalWindow.teachingOrderListStore)
        myGlobalWindow.analysis.UpdateTeachingOrderList(myGlobalWindow.teachingOrderListStore)
        myGlobalWindow.analysis.dataChanged = True
        
        # find letter and select that row in the new teaching order
        for row in myGlobalWindow.teachingOrderListStore:
            if row[0] == myGlobalWindow.letterDragged:
                # any one of these 3 methods works, but shifts selection to top of TreeView
                #treeview.set_cursor(row.path)
                #myGlobalWindow.teachingOrderTreeView.get_selection().select_path(row.path)
                #myGlobalWindow.teachingOrderTreeView.get_selection().select_iter(row.iter)
                break
    
    def on_teachingOrderTreeView_change(self, selection):
        '''User changed the lesson that is selected, so enable/disable the Remove Sight Words button.
        Keep lesson text selection in sync.
        
        Parameter: selection - new lesson selected
        '''
        global myGlobalWindow
        (model, row) = selection.get_selected()
        if row is not None:
            letter = model[row][0]
            if letter == "\u2686\u2686":
                # sight word lesson, enable the remove button
                myGlobalWindow.removeSightWordsButton.set_sensitive(True)
            else:
                # regular lesson, disable the remove sight word button
                myGlobalWindow.removeSightWordsButton.set_sensitive(False)
            
            # select equivalent row in lesson texts
            myGlobalWindow.lessonTextsTreeView.get_selection().select_path(model.get_path(row))
            myGlobalWindow.lessonTextsTreeView.set_cursor(model.get_path(row))
    
    def on_lessonTextsTreeView_change(self, selection):
        '''User changed the lesson that is selected, so update the text displayed.
        Keep teaching order selection in sync.
        
        Parameter: selection - new lesson selected
        '''
        global myGlobalWindow
        (model, row) = selection.get_selected()
        if row is not None:
            myGlobalWindow.SaveLessonText(myGlobalWindow.analysis.selectedGrapheme)
            
            # get grapheme for this row
            letter = model[row][0]
            # get path of selected row
            path = model.get_path(row)
            if letter == "\u2686\u2686":
                # this is a sight word lesson, update the selectedGrapheme to the sight word index
                # get index of selected row
                i = path.get_indices()[0]
                letter = myGlobalWindow.analysis.teachingOrder[i]
            myGlobalWindow.analysis.selectedGrapheme = letter
            if isinstance(letter, int):
                # no filter text for sight words
                myGlobalWindow.lessonTextsFilterTextEntry.set_text("")
            else:
                # make the filter text to be the selected letter
                myGlobalWindow.lessonTextsFilterTextEntry.set_text(letter)
            
            # select equivalent row in teaching order
            myGlobalWindow.teachingOrderTreeView.get_selection().select_path(path)
            myGlobalWindow.teachingOrderTreeView.set_cursor(model.get_path(row))
            
            # update the text field on the Lesson Text tab
            buffer = myGlobalWindow.lessonTextsTextBuffer
            txt = myGlobalWindow.analysis.lessonTexts.get(myGlobalWindow.analysis.selectedGrapheme, "")
            # update the buffer, but don't initiate a changed event
            # (because data hasn't actually changed; we just are displaying a different lesson)
            buffer.handler_block_by_func(myGlobalHandler.on_lessonTextsTextBuffer_changed)
            buffer.set_text(txt)
            buffer.handler_unblock_by_func(myGlobalHandler.on_lessonTextsTextBuffer_changed)
            # but still need to mark the text appropriately
            myGlobalWindow.MarkUntaught(buffer)
        
        # try to grab the focus in the TextView (but this doesn't seem to work...)
        myGlobalWindow.lessonTextsTextView.grab_focus()
        # make sure cursor is at the end of any existing text
        myGlobalWindow.lessonTextsTextBuffer.place_cursor(myGlobalWindow.lessonTextsTextBuffer.get_end_iter())
    
    def on_lessonTextsTextBuffer_changed(self, buffer):
        global myGlobalWindow
        myGlobalWindow.MarkUntaught(buffer)
        myGlobalWindow.analysis.dataChanged = True
    
    def on_lessonTextsFilterTextEntry_changed(self, widget):
        global myGlobalWindow
        myGlobalWindow.MarkUntaught(myGlobalWindow.lessonTextsTextBuffer)
    
    def on_notebook_switch_page(self, notebook, tab, index):
        '''User has moved to a different tab (page) in the notebook interface.
        
        Parameters: index - index of the newly selected tab
        '''
        global myGlobalNotebookPage
        global myGlobalWindow
        global myGlobalBuilder
        if index != myGlobalNotebookPage:
            # there has actually been a change in page, so process it
            if index == 2:
                # transitioning to the Lesson Texts tab, make sure that the text tagging is up-to-date
                myGlobalWindow.MarkUntaught(myGlobalWindow.lessonTextsTextBuffer)
            if myGlobalNotebookPage == 0 and index >= 1:
                # moving from word discovery to a page where we need to display the teaching order
                if myGlobalWindow.analysis.teachingOrderChanged:
                    # if data has changed, calculate a new teaching order
                    myGlobalWindow.analysis.CalculateTeachingOrder(myGlobalWindow.affixesExcluded.get_active(),
                                                                   myGlobalWindow.countEachWord.get_active())
                    myGlobalWindow.analysis.UpdateTeachingOrderList(myGlobalWindow.teachingOrderListStore)
                    # reset the selection of the Teaching Order to the beginning of the lists
                    treeview = myGlobalWindow.teachingOrderTreeView
                    treeview.get_selection().select_path(Gtk.TreePath("0"))
                    treeview = myGlobalWindow.lessonTextsTreeView
                    treeview.get_selection().select_path(Gtk.TreePath("0"))
                    # allow the teaching order to be saved
                    menu = myGlobalBuilder.get_object("saveTeachingOrderMenuItem")
                    menu.set_sensitive(True)
            elif myGlobalNotebookPage >= 1 and index == 0:
                # moving from a teaching order page back to word discovery, give warning that changes could cause loss of some information
                title = _("Warning")
                msg = _("""If you make changes on this Word Discovery page, you may lose
some changes in your Teaching Order, specifically your sight word
lessons and the current teaching order.""")
                SimpleMessage(title, 'dialog-warning', msg)
            # remember which page we are on now
            myGlobalNotebookPage = index


class PrimerPrepWindow:
    '''PrimerPrepWindow class - main class used to run the PrimerPrep program
    
    Creating an instance of this class creates the main PrimerPrep window, and
    calling the method .main() allows it to process all of the menu requests.
    
    Attributes:
      window - Gtk.Window object, main PrimerPrep window
      analysis - WordAnalysis object, calculates and stores word statistics
      wordListStore - ListStore object, holds word list
      wordTreeView - TreeView object, displays word list
      teachingOrderListStore - ListStore object, holds teaching order
      teachingOrderTreeView - TreeView object, displays teaching order
      lessonTextsTreeView - TreeView object, displays teaching order for the Lesson Texts tab
    '''
    
    def WriteFile(self, filename, filetext, containsNFC, containsNFD):
        '''Internal class routine for writing the given text to the given file.
        The check for a pre-existing file will have been done before calling this method.
        User will be notified of any errors in writing the file.
        
        Parameters: filename (str) - full file name/path
                    filetext (str) - multiline string of contents of file to write
        '''
        logger.debug('Saving as:', filename)
        
        if containsNFC:
            if not containsNFD:
                # the data needs to be written out in NFC format
                filetext = unicodedata.normalize('NFC', filetext)
            else:
                # warn the user that data is written out decomposed
                title = _("Encoding error")
                msg = _("""Warning: This is a reminder that your input data has inconsistent encoding,
with some characters composed and some decomposed. This data will be saved in
decomposed format, which may be different than your original source files.""")
                SimpleMessage(title, 'dialog-warning', msg)
        try:
            save_file = open(filename, 'w', encoding='utf-8')
            # write a byte-order mark (BOM) for better file identification
            save_file.write('\ufeff')
            save_file.write(filetext)
            save_file.close()
        except Exception:
            title = _("Error")
            msg = _("Error. File could not be written.")
            SimpleMessage(title, 'dialog-error', msg)
    
    def NewProject(self):
        '''Create a new project (after confirmation not to save existing data). We want
        to really start from scratch, including all configuration information. The easiest
        way to do this is to just delete the WordAnalysis object instance and create a new one.
        '''
        global myGlobalBuilder
        global myGlobalProjectName
        
        if self.analysis.dataChanged:
            # confirm clearing data
            title = _("Confirm clear data")
            msg = _("There is unsaved data. Start a new project anyway?")
            if not SimpleYNQuestion(title, 'dialog-warning', msg):
                # no, we shouldn't clear this data
                return
        # either data hasn't changed since last save or user confirmed to continue anyway
        
        # get rid of the old WordAnalysis object
        del self.analysis
        # create a new instance of WordAnalysis to store our data
        self.analysis = WordAnalysis()
        # we need to set the value of separateCombDiacritics properly from check button
        self.analysis.separateCombDiacritics = myGlobalBuilder.get_object('separateDiacriticsCheckButton').get_active()
        # the affix list has been cleared, so make sure it is cleared in the interface
        self.UpdateAffixList()
        
        # prevent the non-existant project or teaching order from being saved
        menu = myGlobalBuilder.get_object("saveProjectMenuItem")
        menu.set_sensitive(False)
        menu = myGlobalBuilder.get_object("saveTeachingOrderMenuItem")
        menu.set_sensitive(False)
        
        # clear out list stores and update status bar
        fileList = myGlobalBuilder.get_object("fileListStore")
        fileList.clear()
        self.filterTextEntry.set_text("")
        self.wordListStore.clear()
        # clear the text, so we don't try to mark untaught residue
        text = myGlobalBuilder.get_object("lessonTextsTextBuffer")
        text.set_text("")
        self.teachingOrderListStore.clear()
        self.ShowSummaryStatusBar()
        # make sure there is no project name, including in the window title
        myGlobalProjectName = ""
        self.window.set_title("PrimerPrep")
        # may not be on the first notebook tab, but can't change without warning so just leave it...
    
    def SaveProject(self):
        '''Save the project configuration, using the already specified filename
        (so this must follow an Open or Save As command to have a valid filename and path).
        All data structures are stored (using pickle), so they can be restored later.
        '''
        global myGlobalProjectName
        global myGlobalProjectPath
        global myGlobalWindow
        global myGlobalRenderer
        
        # make sure that the project name is valid
        projectExtPattern = r'.+\.ppdata$'
        if not re.match(projectExtPattern, myGlobalProjectName):
            # invalid file name (but this shouldn't happen...)
            title = _("Error")
            msg = _("Invalid file name.")
            SimpleMessage(title, "dialog-error", msg)
            return
        filename = os.path.join(myGlobalProjectPath, myGlobalProjectName)
        # save the project with the dataChanged value indicating no need to save
        self.analysis.dataChanged = False
        # save all of the important data structures to the file, serializing them with pickle
        try:
            with open(filename, 'wb') as f:
                # make sure current lesson text is saved
                self.SaveLessonText(myGlobalWindow.analysis.selectedGrapheme)
                self.analysis.selectedGrapheme = None
                
                # save all of the data into this project backup file
                pickle.dump(dataModelVersion, f)
                pickle.dump(self.analysis, f)
                options = (myGlobalRenderer.fontName, self.affixesExcluded.get_active(),
                           self.countEachWord.get_active())
                pickle.dump(options, f)
        except (OSError, EOFError, pickle.PicklingError) as e:
            # general error writing the file
            title = _("Error")
            msg = _("Error writing project: ") + str(e)
            SimpleMessage(title, "dialog-error", msg)
    
    def SaveProjectAs(self):
        '''Ask user for a filename and save the entire project configuration to that .ppdata
        file. This allows user to open the project later and continuing where they left off.
        Using a FileChooserDialog, the user specifies the file name and location, and
        all data structures are stored (using pickle), so they can be restored later.
        '''
        global myGlobalProjectPath
        global myGlobalPath
        global myGlobalProjectName
        global myGlobalBuilder
        
        msg = _("Save project as...")
        chooser = Gtk.FileChooserDialog(title=msg, parent=self.window,
                                        action=Gtk.FileChooserAction.SAVE)
        chooser.add_buttons(Gtk.STOCK_SAVE, Gtk.ResponseType.OK,
                            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        chooser.set_current_name(_("project.ppdata"))
        if not myGlobalProjectPath:
            # start with the default if we haven't yet loaded a project
            myGlobalProjectPath = myGlobalPath
        chooser.set_current_folder(myGlobalProjectPath)
        chooser.set_do_overwrite_confirmation(True)
        chooser.set_default_response(Gtk.ResponseType.OK)
        filter = Gtk.FileFilter()
        filter.set_name(_("PrimerPrep project files"))
        filter.add_pattern("*.ppdata")
        chooser.add_filter(filter)
        
        while chooser.run() == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            if not filename.endswith(".ppdata"):
                # invalid file name - it must have a .ppdata extenstion at the end
                title = _("Error")
                msg = _("You must use a file name extension of .ppdata for your project.")
                SimpleMessage(title, "dialog-error", msg)
                # add the proper extension
                chooser.set_current_name(os.path.basename(filename) + ".ppdata")
                continue
            # save the path and filename (and update myGlobalPath)
            myGlobalProjectPath = os.path.dirname(filename)
            myGlobalPath = myGlobalProjectPath
            myGlobalProjectName = os.path.basename(filename)
            self.window.set_title(myGlobalProjectName + " — PrimerPrep")
            menu = myGlobalBuilder.get_object("saveProjectMenuItem")
            menu.set_sensitive(True)
            # now that we have the filename and path, just use the standard Save Project code
            self.SaveProject()
            break
        chooser.destroy()
    
    def LoadProject(self, filename):
        global myGlobalRenderer
        global myGlobalProjectPath
        global myGlobalPath
        global myGlobalProjectName
        global myGlobalBuilder
        
        logger.debug("Opening: {}".format(filename))
        try:
            with open(filename, 'rb') as f:
                vernum = pickle.load(f)
                if not isinstance(vernum, int) or vernum not in (1, 2, ):
                    # this is not a project file that we know how to load
                    raise UnknownProjectType
                
                del self.analysis
                self.analysis = pickle.load(f)
                
                # initially there are no changes (so you can quit without confirmation)
                # but note that teachingOrderChanged could be true, so rebuild might be necessary
                self.analysis.dataChanged = False
                
                if vernum == 1:
                    # new fields need to be added
                    self.analysis.containsNFC = False
                    self.analysis.containsNFD = False
                    self.analysis.userInformedEncodingError = False
                    # we need to make sure that all data is NFD
                    fileLinesNFD = []
                    for lines in self.analysis.fileLines:
                        # process this list of text lines (from each file)
                        # sets containsNFC and NFD and gives warning if inconsistent
                        self.analysis.CheckEncoding(lines)
                        # make sure this data (set of lines) is in NFD encoding
                        linesNFD = [unicodedata.normalize('NFD', line) for line in lines]
                        # add this normalized set of text lines to the files list
                        fileLinesNFD.append(linesNFD)
                    # save the normalized text lines as the new
                    self.analysis.fileLines = fileLinesNFD
                    self.analysis.dataChanged = True
                else:
                    if self.analysis.containsNFC and self.analysis.containsNFD:
                        # warn the user that this data contains inconsistent encoding
                        title = _("Encoding error")
                        msg = _("""Warning: This is a reminder that your input data has inconsistent encoding,
with some characters composed and some decomposed. Ask a consultant to help you
make your data more consistent. Any outputs from PrimerPrep (word list, teaching order)
will be output in decomposed format.""")
                        SimpleMessage(title, 'dialog-warning', msg)
                
                # load and unpack the options tuple, and set the options
                options = pickle.load(f)
                # set the new font, and make sure it gets applied through the window
                myGlobalRenderer.SetFont(options[0])
                self.ApplyNewFont()
                # set other options
                self.affixesExcluded.set_active(options[1])
                self.countEachWord.set_active(options[2])
            
            # save the path and filename (and update myGlobalPath)
            myGlobalProjectPath = os.path.dirname(filename)
            myGlobalPath = myGlobalProjectPath
            myGlobalProjectName = os.path.basename(filename)
            self.window.set_title(myGlobalProjectName + " — PrimerPrep")
            
            # from the loaded analysis data, set the checkbox for separate diacritics
            sepDiacr = myGlobalBuilder.get_object("separateDiacriticsCheckButton")
            sepDiacr.set_active(self.analysis.separateCombDiacritics)
            
            # from the loaded analysis data, update all of the ListStores
            self.analysis.UpdateFileList(self.fileListStore,
                                         myGlobalBuilder.get_object('showFullPathCheckButton').get_active())
            self.analysis.UpdateWordList(self.wordListStore)
            self.analysis.UpdateTeachingOrderList(self.teachingOrderListStore)
            self.UpdateAffixList()
            self.ShowSummaryStatusBar()
            
            # allow the project to be saved
            menu = myGlobalBuilder.get_object("saveProjectMenuItem")
            menu.set_sensitive(True)
            # allow the teaching order to be saved if project has one
            menu = myGlobalBuilder.get_object("saveTeachingOrderMenuItem")
            if hasattr(self.analysis, 'teachingOrder'):
                menu.set_sensitive(True)
            else:
                menu.set_sensitive(False)
            
            # because teaching order rebuild may be necessary, it's good to start on first notebook tab
            self.mainNB.set_current_page(0)
        except (OSError, EOFError, pickle.UnpicklingError) as e:
            # general error reading the file
            title = _("Error")
            msg = _("Error reading project: ") + str(e)
            SimpleMessage(title, "dialog-error", msg)
        except UnknownProjectType:
            # unknown type of project file
            title = _("Error")
            msg = _("This file does not contain valid project data.")
            SimpleMessage(title, "dialog-error", msg)
    
    def OpenProject(self):
        '''Allow the user to open a previously saved file and load the project data. Using a
        FileChooserDialog, the user locates and selects the project file to be loaded.
        All data structures are restored (using pickle).
        '''
        global myGlobalProjectPath
        global myGlobalPath
        
        if self.analysis.dataChanged:
            # confirm clearing data
            title = _("Confirm clear data")
            msg = _("There is unsaved data. Open a project anyway?")
            if not SimpleYNQuestion(title, 'dialog-warning', msg):
                # no, we shouldn't quit
                return
        # either data hasn't changed since last save or user confirmed to continue anyway
        
        msg = _("Choose project to open...")
        chooser = Gtk.FileChooserDialog(title=msg, parent=self.window,
                                        action=Gtk.FileChooserAction.OPEN)
        chooser.add_buttons(Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
                            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        chooser.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        chooser.set_default_response(Gtk.ResponseType.CANCEL)
        chooser.set_select_multiple(False)
        if not myGlobalProjectPath:
            # start with the default if we haven't yet loaded a project
            myGlobalProjectPath = myGlobalPath
        chooser.set_current_folder(myGlobalProjectPath)
        
        filter = Gtk.FileFilter()
        filter.set_name(_("PrimerPrep project files"))
        filter.add_pattern("*.ppdata")
        chooser.add_filter(filter)
        # this only allows .ppdata files to be selected, so no filename check required
        
        if chooser.run() == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            if filename:
                self.LoadProject(filename)
        chooser.destroy()
    
    def AddTexts(self):
        '''Process an Add Text(s) button click. Using a FileChooserDialog, the
        user locates and selects the file(s) to be loaded into the analysis.
        Note that multiple files (in the same directory) can be selected, and
        each file selected will be loaded into the analysis.
        
        Parameters: widget (unused)
                    data (unused)
        '''
        global myGlobalBuilder
        
        msg = _("Choose text(s) to open...")
        chooser = Gtk.FileChooserDialog(title=msg, parent=self.window,
                                        action=Gtk.FileChooserAction.OPEN)
        chooser.add_buttons(Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
                            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        chooser.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        chooser.set_default_response(Gtk.ResponseType.CANCEL)
        chooser.set_select_multiple(True)
        
        # set up file filters for the chooser
        filter = Gtk.FileFilter()
        filter.set_name(_("Text files"))
        filter.add_pattern("*.txt")
        filter.add_pattern("*.sfm")
        chooser.add_filter(filter)

        filter = Gtk.FileFilter()
        filter.set_name(_("All files"))
        filter.add_pattern("*")
        chooser.add_filter(filter)
        
        if chooser.run() == Gtk.ResponseType.OK:
            filenames = chooser.get_filenames()
            fileLoaded = False
            for filename in filenames:
                #logger.debug('Loading:', filename.encode('utf-8'))
                if self.analysis.AddWordsFromFile(filename):
                    # loaded successfully
                    fileLoaded = True
                    if myGlobalBuilder.get_object('showFullPathCheckButton').get_active():
                        name = filename
                    else:
                        name = filename.split('\\')[-1]
                    myGlobalBuilder.get_object('fileListStore').append([name])
                    self.analysis.dataChanged = True
            if fileLoaded:
                # at least one loaded, update data on screen
                self.analysis.UpdateWordList(self.wordListStore)
                self.ShowSummaryStatusBar()
        chooser.destroy()
    
    def _save_normalized_lessontext(self, buffer, textNFD):
        # set_text, which will emit "changed" and call MarkUntaught again
        buffer.set_text(textNFD)
        return False  # Stop idle_add
    
    def MarkUntaught(self, buffer):
        '''The lesson text changed. Tag untaught words/letters with 'self.untaughtTag'.
        This involves checking individual words for sight words, and individual graphemes.
        
        Parameters: buffer - TextBuffer
        TODO: If a lesson has a character that doesn't appear at all in the loaded texts,
        it is treated as untaught residue. Is that correct?
        '''
        # first check buffer for any NFC characters, and convert them to NFD
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False).lower()
        textNFD = unicodedata.normalize('NFD', text)
        if (text != textNFD):
            # defer normalization so we don't modify the buffer inside a signal handler
            GLib.idle_add(self._save_normalized_lessontext, buffer, textNFD)
            return
        
        # find out which lesson is selected, to know what letters/sight words have been taught
        sel = self.teachingOrderTreeView.get_selection()
        (model, row) = sel.get_selected()
        if row is None or not hasattr(self.analysis, 'teachingOrder'):
            # there is no row selected, or there is no teachingOrder,
            # so whatever is there should be marked as untaught residue
            # this probably only happens when there is an empty teaching order...
            buffer.apply_tag(self.untaughtTag, buffer.get_start_iter(), buffer.get_end_iter())
            return
        
        # get path and index of selected row
        path = model.get_path(row)
        idx = path.get_indices()[0]
        
        # create a list of the graphemes taught and make a set (for faster lookup) of sight words
        graphemesTaughtList = []
        sightWords = set()
        for i in range(idx+1):
            letter = self.analysis.teachingOrder[i]
            if isinstance(letter, int):
                # this is actually a placeholder for sightwords, so add them (in lower case) to the dictionary
                for sw in self.analysis.sightWords[letter-1]:
                    # remove any hyphens from affix sight words, as that leads to better marking of untaught residue
                    if sw.startswith('-'):
                        sw = sw[1:]
                    if sw.endswith('-'):
                        sw = sw[:-1]
                    # if not empty (hyphen by itself?) save in dictionary
                    if len(sw) > 0:
                        sightWords.add(sw.lower())
            else:
                graphemesTaughtList.append(letter)
        
        # create a list of the graphemes NOT taught
        graphemesUntaughtList = []
        for i in range(idx+1, len(self.analysis.teachingOrder)):
            letter = self.analysis.teachingOrder[i]
            if isinstance(letter, int):
                # do nothing with untaught sightwords
                pass
            else:
                graphemesUntaughtList.append(letter)
        
        # create a regex for finding all graphemes, with longest graphemes first so that multigraphs match
        # Note: RegEx's don't need ^ at the start because we use re.match, which only matches at the beginning of the string
        allGraphemesList = graphemesTaughtList + graphemesUntaughtList
        allGraphemesList.sort(key=len, reverse=True)
        allGraphemesRegEx = '|'.join(allGraphemesList)
        findAllGraphemes = re.compile('(' + allGraphemesRegEx + ')')
        
        # quick way to tell if grapheme found has been taught or not
        graphemesTaughtSet = set(graphemesTaughtList)
        
        # build 'wordBreaks' string with all word breaking characters for RegEx splitting
        wordBreaks = ''
        for char in self.analysis.wordBreakChars:
            # need to put '\' before special characters
            if char in '.^$*+-?{}\\[]|()':
                wordBreaks = wordBreaks + '\\'
            wordBreaks = wordBreaks + char
        # add line breaks as well, since they don't seem to be in the wordBreakChars list
        wordBreaks += '\n\r'
        
        # a regex for finding words
        findWord = re.compile('[^' + wordBreaks + ']+')
        # create a set of words already taught in previous lessons
        wordsPrevUsed = set()
        for i in range(idx):
            letter = self.analysis.teachingOrder[i]
            txt = self.analysis.lessonTexts.get(letter, "")
            wordsPrevUsed.update(word.lower() for word in findWord.findall(txt))
        
        # remove existing "filter" and "newWord" tags
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        buffer.remove_tag_by_name("filter", start_iter, end_iter)
        buffer.remove_tag_by_name("newWord", start_iter, end_iter)
        
        # get the buffer text to process
        text = buffer.get_text(start_iter, end_iter, False).lower()
        # the text should already be NFD, but this is a final safety check
        textNFD = unicodedata.normalize('NFD', text)
        if (text != textNFD):
            raise RuntimeError("Found unexpected NFC text")
        
        # tag all text that matches the user-entered filter string
        filter_text = self.lessonTextsFilterTextEntry.get_text().lower().strip()
        if filter_text:
            # there IS text to highlight, so find and tag all matches with "filter"
            search_pos = 0
            while True:
                index = text.find(filter_text, search_pos)
                if index == -1:
                    break       # no more
                # convert offset (int) to Gtk.TextIter range
                match_start = buffer.get_iter_at_offset(index)
                match_end = buffer.get_iter_at_offset(index + len(filter_text))
                buffer.apply_tag(self.filterTag, match_start, match_end)
                # start after that match
                search_pos = index + len(filter_text)
        
        # initialize loop variables
        pos = 0
        secStart = 0
        # start in "taught" section
        inTaughtSection = True
        
        # create a regex for finding the next word chunk
        findWordChunk = re.compile(r'(.*?)([' + wordBreaks + ']+|$)')
        
        # loop over entire text
        # - find the next word, up to the next wordbreak character(s), and see if it's a sightword
        # - if sightword, mark as taught
        # - if not, go through the word one grapheme at a time and mark taught/untaught as appropriate
        # - wordbreak characters are considered taught
        
        while pos < len(text):
            # find next word (this will always match, but sometimes will give empty string)
            m = findWordChunk.match(text, pos)
            nextWord = m.group(1)
            # get the length of the word
            wordLength = len(nextWord)
            wordBreaksLength = len(m.group(2))
            endWordPos = pos + wordLength
            if nextWord not in wordsPrevUsed:
                match_start = buffer.get_iter_at_offset(pos)
                match_end = buffer.get_iter_at_offset(endWordPos)
                buffer.apply_tag(self.newWordTag, match_start, match_end)
            if nextWord in sightWords:
                logger.debug("taught sightword ({}-{})".format(pos, endWordPos))
                # we were already in (taught) wordbreak characters, so just continue
                pos = endWordPos
                continue
            # not a sightword, so just process the graphemes in this word one by one
            while pos < endWordPos:
                m = findAllGraphemes.match(text, pos)
                if not m:
                    # grapheme not found, so must be untaught
                    # (should only happen if it's a character not in the loaded texts?)
                    if inTaughtSection:
                        # switch taught/untaught section
                        if pos > secStart:
                            buffer.remove_tag(self.untaughtTag,
                                              buffer.get_iter_at_offset(secStart), 
                                              buffer.get_iter_at_offset(pos))
                            logger.debug("taught ({}-{})".format(secStart, pos))
                            secStart = pos
                        inTaughtSection = False
                    # move to the next character
                    pos += 1
                else:
                    # grapheme was found
                    gr = m.group(1)
                    if gr in graphemesTaughtSet:
                        # this grapheme has already been taught
                        if not inTaughtSection:
                            # switch taught/untaught section
                            if pos > secStart:
                                buffer.apply_tag(self.untaughtTag,
                                                  buffer.get_iter_at_offset(secStart), 
                                                  buffer.get_iter_at_offset(pos))
                                logger.debug("untaught ({}-{})".format(secStart, pos))
                                secStart = pos
                            inTaughtSection = True
                    else:
                        # this grapheme hasn't been taught
                        if inTaughtSection:
                            # switch taught/untaught section
                            if pos > secStart:
                                buffer.remove_tag(self.untaughtTag,
                                                  buffer.get_iter_at_offset(secStart), 
                                                  buffer.get_iter_at_offset(pos))
                                logger.debug("taught ({}-{})".format(secStart, pos))
                                secStart = pos
                            inTaughtSection = False
                    # move past this grapheme
                    pos += len(gr)
            # move the pos pointer past wordBreaks
            if wordBreaksLength > 0:
                # close any open untaught section
                if not inTaughtSection:
                    # switch taught/untaught section
                    if pos > secStart:
                        buffer.apply_tag(self.untaughtTag,
                                          buffer.get_iter_at_offset(secStart), 
                                          buffer.get_iter_at_offset(pos))
                        logger.debug("untaught ({}-{})".format(secStart, pos))
                        secStart = pos
                    inTaughtSection = True
                pos += wordBreaksLength
                    
        # report final section
        if inTaughtSection:
            if pos > secStart:
                buffer.remove_tag(self.untaughtTag,
                                  buffer.get_iter_at_offset(secStart), 
                                  buffer.get_iter_at_offset(pos))
                logger.debug("taught ({}-{})".format(secStart, pos))
        else:
            if pos > secStart:
                buffer.apply_tag(self.untaughtTag,
                                  buffer.get_iter_at_offset(secStart), 
                                  buffer.get_iter_at_offset(pos))
                logger.debug("untaught ({}-{})".format(secStart, pos))
        
    def SaveLessonText(self, grapheme):
        # save out the current text into the entry for the previously selected grapheme
        if self.analysis.selectedGrapheme is not None:
            s = self.lessonTextsTextBuffer.get_start_iter()
            e = self.lessonTextsTextBuffer.get_end_iter()
            self.analysis.lessonTexts[grapheme] = self.lessonTextsTextBuffer.get_text(s, e, False)
    
    def UpdateAffixList(self):
        # update the affix list field with new affixes (add/remove vernacular class, as necessary)
        if len(self.analysis.affixes) > 0:
            # there are some affixes, so display them
            affixes = ' '.join(self.analysis.affixes)
            # affixes.replace('-', '\u2013')
            # break the lines only on spaces (auto-breaking sometimes puts suffix hyphen at end of row)
            affixes = re.sub('(.{30,40}) ', '\\1\n', affixes)
            self.affixList.get_style_context().add_class("vernacular")
        else:
            affixes = _("<i>empty</i>")
            self.affixList.get_style_context().remove_class("vernacular")
        self.affixList.set_markup(affixes)
    
    def ApplyNewFont(self):
        # apply a new vernacular font, primarily updating the CellRendererText properties
        global myGlobalRenderer
        
        # process affixes again, in case we switched between fonts that need/don't need ZWJ
        self.UpdateAffixList()
        self.analysis.ProcessAffixes()
        self.analysis.UpdateWordList(self.wordListStore)
        
        self.wordListWordCellRenderer.set_property('font-desc', myGlobalRenderer.vernFontDesc)
        self.teachingOrderLetterCellRenderer.set_property('font-desc', myGlobalRenderer.vernFontDesc)
        self.teachingOrderExamplesCellRenderer.set_property('font-desc', myGlobalRenderer.vernFontDesc)
        self.lessonTextsLetterCellRenderer.set_property('font-desc', myGlobalRenderer.vernFontDesc)
        # need to do this additional step to make sure that resized fonts are handled appropriately
        self.wordListTreeView.get_column(0).queue_resize()
        self.teachingOrderTreeView.get_column(0).queue_resize()
        self.lessonTextsTreeView.get_column(0).queue_resize()
        
    def VisibleItem(self, model, row, data=None):
        # get the filter text from the filter Entry field
        filterText = self.filterTextEntry.get_text().lower()
        
        # an empty filter matches everything
        if filterText == "":
            return True
        
        # get the word to check if it's visible
        word = model.get_value(row, 0).lower()
        # remove all of the formatting
        word = word.replace('<b>', '')
        word = word.replace('</b>', '')
        word = word.replace('<span foreground="gray">', '')
        word = word.replace('</span>', '')
        # see if the filter text is in this word of the word list
        return filterText in word
    
    def WordListCompareWord(self, model, row1, row2, user_data):
        # have to use get_model to get from TreeModelFilter down to ListStore
        #sort_column, _ = model.get_model().get_sort_column_id()
        value1 = model.get_value(row1, 0)
        value2 = model.get_value(row2, 0)
        value1 = value1.replace('<b>', '')
        value1 = value1.replace('</b>', '')
        value1 = value1.replace('<span foreground="gray">', '')
        value1 = value1.replace('</span>', '')
        value2 = value2.replace('<b>', '')
        value2 = value2.replace('</b>', '')
        value2 = value2.replace('<span foreground="gray">', '')
        value2 = value2.replace('</span>', '')
        if value1 < value2:
            return -1
        else:
            return 1
        # don't need equal, as they should never be equal
    
    def WordListCompareFreq(self, model, row1, row2, user_data):
        # have to use get_model to get from TreeModelFilter down to ListStore
        value1 = model.get_value(row1, 1)
        value2 = model.get_value(row2, 1)
        if value1 < value2:
            return -1
        elif value1 == value2:
            value1 = model.get_value(row1, 0)
            value2 = model.get_value(row2, 0)
            value1 = value1.replace('<b>', '')
            value1 = value1.replace('</b>', '')
            value1 = value1.replace('<span foreground="gray">', '')
            value1 = value1.replace('</span>', '')
            value2 = value2.replace('<b>', '')
            value2 = value2.replace('</b>', '')
            value2 = value2.replace('<span foreground="gray">', '')
            value2 = value2.replace('</span>', '')
            _, sort_type = model.get_model().get_sort_column_id()
            if sort_type == Gtk.SortType.DESCENDING:
                val = 1
            else:
                val = -1
            if value1 < value2:
                return val
            else:
                return -val
            # don't need equal, as they should never be equal
        else:
            return 1
    
    def ShowSummaryStatusBar(self):
        '''Put the number of texts and number of unique words
        (and number filtered, if applicable) in the statusbar.
        '''
        global myGlobalBuilder
        
        totalWords = self.analysis.GetNumWords()
        numFiltered = len(self.wordListTreeModelFilter)
        text = _("Texts") + ": " + str(self.analysis.GetNumFiles())
        text += "  " + _("Unique words") + ": " + str(totalWords)
        if numFiltered < totalWords:
            # the list is filtered, so display number of words found
            text += "  ({} ".format(numFiltered) + _("filtered") + ")"
        statusbar = myGlobalBuilder.get_object("statusbar")
        statusbar.push(0, text)
    
    def letter_cell_data_func(self, column, cell, model, iter, data):
        global myGlobalRenderer
        
        content = model.get_value(iter, 0)
    
        if content == '\u2686\u2686':
            vernFontDesc = Pango.FontDescription("DejaVu Sans 14")
            cell.set_property('font-desc', vernFontDesc)
        else:
            cell.set_property('font-desc', myGlobalRenderer.vernFontDesc)

    def __init__(self):
        '''Initialize this PrimerPrepWindow object. Creates the window, with
        menus, procedures associated with the menus, and text boxes to hold
        all of the analysis data.
        '''
        global myGlobalBuilder
        global myGlobalHandler
        
        # create an instance of WordAnalysis to store our data
        self.analysis = WordAnalysis()
        
        # keep track of some builder UI objects
        self.window = myGlobalBuilder.get_object("mainWindow")
        self.mainNB = myGlobalBuilder.get_object("mainNB")
        self.affixList = myGlobalBuilder.get_object("affixList")
        self.affixesExcluded = myGlobalBuilder.get_object("affixesExcludedRadioButton")
        self.countEachWord = myGlobalBuilder.get_object("countWordEachTimeRadioButton")
        self.fileListStore = myGlobalBuilder.get_object("fileListStore")
        self.filterTextEntry = myGlobalBuilder.get_object("filterTextEntry")
        self.wordListStore = myGlobalBuilder.get_object("wordListStore")
        self.WordListFilter = myGlobalBuilder.get_object("wordListStore")
        self.wordListTreeView = myGlobalBuilder.get_object("wordListTreeView")
        self.wordListWordCellRenderer = myGlobalBuilder.get_object("wordListWordCellRenderer")
        self.wordListFreqCellRenderer = myGlobalBuilder.get_object("wordListFreqCellRenderer")
        self.wordListTreeModelFilter = myGlobalBuilder.get_object("wordListTreeModelFilter")
        self.teachingOrderListStore = myGlobalBuilder.get_object("teachingOrderListStore")
        self.teachingOrderTreeView = myGlobalBuilder.get_object("teachingOrderTreeView")
        self.teachingOrderLetterColumn = myGlobalBuilder.get_object("teachingOrderLetterColumn")
        self.teachingOrderLetterCellRenderer = myGlobalBuilder.get_object("teachingOrderLetterCellRenderer")
        self.teachingOrderFreqCellRenderer = myGlobalBuilder.get_object("teachingOrderFreqCellRenderer")
        self.teachingOrderExamplesColumn = myGlobalBuilder.get_object("teachingOrderExamplesColumn")
        self.teachingOrderExamplesCellRenderer = myGlobalBuilder.get_object("teachingOrderExamplesCellRenderer")
        self.removeSightWordsButton = myGlobalBuilder.get_object("removeSightWordsButton")
        self.lessonTextsTreeView = myGlobalBuilder.get_object("lessonTextsTreeView")
        self.lessonTextsTextView = myGlobalBuilder.get_object("lessonTextsTextView")
        self.lessonTextsTextBuffer = myGlobalBuilder.get_object("lessonTextsTextBuffer")
        self.lessonTextsLetterColumn = myGlobalBuilder.get_object("lessonTextsLetterColumn")
        self.lessonTextsLetterCellRenderer = myGlobalBuilder.get_object("lessonTextsLetterCellRenderer")
        self.lessonTextsFreqCellRenderer = myGlobalBuilder.get_object("lessonTextsFreqCellRenderer")
        self.lessonTextsFilterTextEntry = myGlobalBuilder.get_object("lessonTextsFilterTextEntry")
        
        # allow markup in the examples column (in teaching order) - clear "text" attribute first
        self.teachingOrderExamplesColumn.clear_attributes(self.teachingOrderExamplesCellRenderer)
        self.teachingOrderExamplesColumn.add_attribute(self.teachingOrderExamplesCellRenderer, "markup", 2)
        
        # prepare the analysis dialogs for future use
        self.theAffixesDialog = AffixesDialog()
        self.theWordBreaksDialog = WordBreaksDialog()
        self.theDigraphsDialog = DigraphsDialog()
        self.theWordEditDialog = WordEditDialog()
        self.theSightWordsDialog = SightWordsDialog()
        self.theConcordanceDialog = ConcordanceDialog()
        self.theConfigureSFMDialog = ConfigureSFMDialog()
        
        # set the default UI font, based on OS
        if platform.system() == "Windows":
            self.window.get_settings().set_property('gtk-font-name', 'Segoe UI 12')
        else:
            self.window.get_settings().set_property('gtk-font-name', 'Ubuntu 12')
        
        # add a vernacular class to vernacular fields (the TreeViews are handled manually in ApplyFonts)
        self.filterTextEntry.get_style_context().add_class("vernacular")
        self.lessonTextsTextView.get_style_context().add_class("vernacular")
        self.lessonTextsFilterTextEntry.get_style_context().add_class("vernacular")
        # set the vernacular font
        self.ApplyNewFont()
        
        self.window.set_default_direction(Gtk.TextDirection.LTR)
        self.isRTL = False
        # this event is set as default in the .glade file for startup
        #self.window.connect("delete-event", myGlobalHandler.on_mainWindow_delete_event)
        
        # show the main PrimerPrep window
        self.window.show_all()
        
        # disable certain options (these are set as defaults in the .glade file for startup)
        #menu = myGlobalBuilder.get_object("saveProjectMenuItem")
        #menu.set_sensitive(False)
        #menu = myGlobalBuilder.get_object("saveTeachingOrderMenuItem")
        #menu.set_sensitive(False)
        #button = myGlobalBuilder.get_object("removeSightWordsButton")
        #button.set_sensitive(False)
        
        # set word list visible function to watch the Filter entry
        self.wordListTreeModelFilter.set_visible_func(self.VisibleItem)
        # set our specialized word/frequency sort functions
        wordListTreeModelSort = myGlobalBuilder.get_object("wordListTreeModelSort")
        wordListTreeModelSort.set_sort_func(0, self.WordListCompareWord, None)
        wordListTreeModelSort.set_sort_func(1, self.WordListCompareFreq, None)
        
        # when a row of the teaching order treeview is selected, it emits a signal
        teachingOrderSelection = self.teachingOrderTreeView.get_selection()
        teachingOrderSelection.connect("changed", myGlobalHandler.on_teachingOrderTreeView_change)
        
        # when a row of the lesson texts treeview is selected, it emits a signal
        lessonTextSelection = self.lessonTextsTreeView.get_selection()
        lessonTextSelection.connect("changed", myGlobalHandler.on_lessonTextsTreeView_change)
        
        # need a special handler for the letter column (in teaching order and lesson texts) to set font for sightwords symbol
        self.teachingOrderLetterColumn.set_cell_data_func(self.teachingOrderLetterCellRenderer, self.letter_cell_data_func)
        self.lessonTextsLetterColumn.set_cell_data_func(self.lessonTextsLetterCellRenderer, self.letter_cell_data_func)
        
        # set up a tag for untaught residue
        textBuffer = myGlobalBuilder.get_object("lessonTextsTextBuffer")
        self.untaughtTag = textBuffer.create_tag("untaught", foreground="red")
        self.filterTag = textBuffer.create_tag("filter", weight=Pango.Weight.BOLD)
        self.newWordTag = textBuffer.create_tag("newWord", background="lightyellow")
        
        self.ShowSummaryStatusBar()


def SaveConfig():
    '''Save out the current config file.  Done whenever there is a change.'''
    global myGlobalConfigFile
    global myGlobalConfig
    with open(myGlobalConfigFile, 'w') as configfile:
        myGlobalConfig.write(configfile)        


# If the program is run directly or passed as an argument to the python
# interpreter then create a PrimerPrepWindow class instance and run it
if __name__ == "__main__":
    # prep to display a splash screen, especially since the opening of the initial window can take some time
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        myGlobalProgramPath = sys._MEIPASS
        # running in a PyInstaller bundle
        cmds = [os.path.join(myGlobalProgramPath, 'PrimerPrepSplash')]
    else:
        myGlobalProgramPath = os.path.dirname(os.path.abspath(__file__))
        cmds = [sys.executable, os.path.join(myGlobalProgramPath, "PrimerPrepSplash.py")]
    # set the current working directory to the app directory
    os.chdir(myGlobalProgramPath)
    #print('Splash:', cmds)
    try:
        splashScreen = subprocess.Popen(cmds)
    except:
        splashScreen = None
    
    # initialize our global variables
    myGlobalPath = os.path.expanduser("~")
    if platform.system() == "Windows":
        #  for Windows, add Documents to the default path
        myGlobalPath = os.path.join(myGlobalPath, 'Documents')
    
    # make sure we have our default English translation set up
    locale_path = os.path.join(myGlobalProgramPath, 'translations')
    # a list of translation languages, each with a tuple
    # (code, menu text, font (blank for default), direction (LTR or RTL), translation engine)
    translation_languages = []
    translation_languages.append( ( 'en_US', 'English Interface', '', 'LTR',
                                    gettext.translation(APP_NAME, locale_path, languages=['en_US'], fallback = True) ) )
    translation_languages.append( ( 'fr_FR', 'Interface française', '', 'LTR',
                                    gettext.translation(APP_NAME, locale_path, languages=['fr_FR'], fallback = True) ) )
    # set English as default language to start with
    _ = translation_languages[0][4].gettext
    
    # initialize the global builder first, as we need to look up objects in our setup
    myGlobalBuilder = GtkBuilder("PrimerPrep.glade", APP_NAME)
    myGlobalHandler = Handler()
    myGlobalBuilder.connect_signals(myGlobalHandler)
    
    # check for an argument (project to open)
    filename = None
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not filename.endswith(".ppdata"):
            if splashScreen:
                splashScreen.terminate()
            msg = _("""The input file provided to PrimerPrep is not a valid project file.
It should have a .ppdata extension.""") + " ( " + filename + " )"
            SimpleMessage(_("Invalid input file"), "dialog-error", msg)
            sys.exit(1)
    
    # initialize the renderer (and also set up CSS style providers) before the window, since window code needs it
    myGlobalRenderer = VernacularRenderer()
    myGlobalWindow = PrimerPrepWindow()
    
    # make sure the English and French interface menu items are connected to the Handler
    menuItem = myGlobalBuilder.get_object("englishInterfaceMenuItem")
    menuItem.connect("activate", myGlobalHandler.on_interfaceMenuItem_activate, 'en_US', 0)
    menuItem = myGlobalBuilder.get_object("frenchInterfaceMenuItem")
    menuItem.connect("activate", myGlobalHandler.on_interfaceMenuItem_activate, 'fr_FR', 1)
    
    # for internationalization, we load languages from .json file
    with open(os.path.join(locale_path, 'langs.json'), 'r', encoding='utf-8') as f:
        langs = json.load(f)
    
    # create menu items for any languages beyond English or French
    configMenu = myGlobalBuilder.get_object("configureMenu")
    EnglishInterfaceMenu = myGlobalBuilder.get_object("englishInterfaceMenuItem")
    for lang in sorted(langs):
        if lang == 'en_US' or lang == 'fr_FR':
            # we already dealt with these
            continue
        translation_languages.append( ( lang, langs[lang][0], langs[lang][1], langs[lang][2],
                                        gettext.translation(APP_NAME, locale_path, languages=[lang], fallback = True) ) )
        menuItem = Gtk.RadioMenuItem.new_with_label_from_widget(EnglishInterfaceMenu, langs[lang][0])
        menuItem.connect("activate", myGlobalHandler.on_interfaceMenuItem_activate, lang, len(translation_languages) - 1)
        configMenu.append(menuItem)
        menuItem.set_visible(True)
    
    # determine the config file location, based on platform
    if platform.system() == "Windows":
        myGlobalConfigFile = os.path.join(os.environ['APPDATA'], 'SIL', 'PrimerPrep')
    else:
        myGlobalConfigFile = os.path.join(myGlobalPath, '.config', 'PrimerPrep')
    # make sure the folder exists, then define the actual config file name (includes the full path)
    os.makedirs(myGlobalConfigFile, exist_ok=True)
    myGlobalConfigFile = os.path.join(myGlobalConfigFile, 'PrimerPrep.ini')
    
    # load environment variables, if doesn't exist return empty dataset
    myGlobalConfig.read(myGlobalConfigFile)
    if 'Option' in myGlobalConfig:
        # config file was found, so process the data
        myGlobalInterface = myGlobalConfig['Option'].get('lang', 'en_US')
        if myGlobalInterface != 'en_US':
            for idx, (code, title, font, direction, engine) in enumerate(translation_languages):
                if code == myGlobalInterface:
                    # assumes there are exactly two Configure menu items before the language radio buttons start
                    configMenu.get_children()[idx+2].activate()
        if myGlobalConfig['Option'].get('excludeaffixes', '1') != '1':
            myGlobalBuilder.get_object("affixesSeparateWordsRadioButton").set_active(True)
        if myGlobalConfig['Option'].get('countallwords', '1') != '1':
            myGlobalBuilder.get_object("countWordOnlyOnceRadioButton").set_active(True)
        if myGlobalConfig['Option'].get('separatecombdia', '0') != '0':
            myGlobalBuilder.get_object("separateDiacriticsCheckButton").set_active(True)
    else:
        # no config file, create a default one and save it out
        myGlobalConfig['Option'] = {'lang': 'en_US',
                                    'digraphautosearch': '1',  # deprecated
                                    'excludeaffixes': '1', 
                                    'countallwords': '1',
                                    'separatecombdia' : '0'}
        # create the .ini file
        SaveConfig()
    
    # just starting so nothing changed yet
    myGlobalWindow.analysis.dataChanged = False
    myGlobalWindow.analysis.teachingOrderChanged = False
    
    # we are done stalling for time
    if splashScreen:
        splashScreen.terminate()
    
    # if a filename was passed (e.g. by double-clicking a .ppdata project data file), load it
    if filename:
        myGlobalWindow.LoadProject(filename)
    
    Gtk.main()

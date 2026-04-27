#!/usr/bin/python3
# 
# lexicon_import

from lxml import etree


def GetLiftHeadwordContainer(entry):
    '''
    Return the preferred form container for headword extraction.
    Prefer <citation>, fall back to <lexical-unit>.
    '''
    citation = entry.find("citation")
    if citation is not None:
        return citation
    return entry.find("lexical-unit")

def LiftLexiconPrep(filename):
    '''
    Scan a LIFT file and return:
        tree      = parsed XML tree
        ws_list   = sorted list of lexical-unit writing systems
    '''
    tree = etree.parse(filename)
    root = tree.getroot()

    ws_set = set()

    for entry in root.findall(".//entry"):
        headword_container = GetLiftHeadwordContainer(entry)
        if headword_container is None:
            continue

        for form in headword_container.findall("form"):
            lang = form.get("lang")
            if lang:
                ws_set.add(lang)

    return tree, sorted(ws_set)

def LoadLiftLexicon(tree, selected_ws):
    '''
    Load lexical entries from parsed LIFT tree.
    Returns:
        [{"lexeme": "...", "pos": "..."}]
    '''
    root = tree.getroot()
    entries = []

    for entry in root.findall(".//entry"):
        headword_container = GetLiftHeadwordContainer(entry)
        if headword_container is None:
            continue
        lexeme = None
        for form in headword_container.findall("form"):
            if form.get("lang") == selected_ws:
                text_node = form.find("text")
                if text_node is not None and text_node.text:
                    lexeme = text_node.text.strip()
                    break
        if not lexeme:
            continue

        pos = ""
        sense = entry.find("sense")
        if sense is not None:
            gram = sense.find("grammatical-info")
            if gram is not None:
                pos = gram.get("value", "")

        entries.append({
            "lexeme": lexeme,
            "pos": pos
        })

    return entries

def LoadSFMLexicon(filename):
    '''
    Load an SFM/Toolbox lexicon file.
    Returns list of tuples: (lexeme, grammatical_info)
    '''
    return []
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

def SFMLexiconPrep(filename):
    '''
    Parse an SFM/Toolbox file and return:
        entries    = list of entries; each entry is a list of (sfm, value) pairs
        lx_markers = sorted list of unique markers starting with "lx"
        pos_markers = sorted list of unique markers starting with "ps"
    A new entry begins whenever the bare "lx" marker is encountered.
    Lines without a leading backslash are continuations of the previous marker.
    '''
    try:
        with open(filename, encoding='utf-8') as f:
            raw_lines = f.readlines()
    except UnicodeDecodeError:
        with open(filename, encoding='latin-1') as f:
            raw_lines = f.readlines()

    entries = []
    current_entry = None
    current_sfm = None
    current_val = None
    lx_set = set()
    pos_set = set()

    def _flush_field():
        if current_sfm is not None and current_entry is not None:
            current_entry.append((current_sfm, current_val))

    for line in raw_lines:
        line = line.rstrip('\n\r')
        if not line.strip():
            continue

        if line.startswith('\\'):
            _flush_field()
            parts = line[1:].split(None, 1)
            current_sfm = parts[0]
            current_val = parts[1].strip() if len(parts) > 1 else ''

            if current_sfm == 'lx':
                if current_entry is not None:
                    entries.append(current_entry)
                current_entry = []

            if current_sfm.startswith('lx'):
                lx_set.add(current_sfm)
            elif current_sfm.startswith('ps'):
                pos_set.add(current_sfm)
        else:
            # continuation line
            if current_val is not None:
                current_val = current_val + ' ' + line.strip()

    _flush_field()
    if current_entry is not None:
        entries.append(current_entry)

    return entries, sorted(lx_set), sorted(pos_set)


def LoadSFMLexicon(entries, selected_lx, selected_pos):
    '''
    Load lexical entries from parsed SFM entries.
    selected_lx:  the sfm marker to use for the lexeme (e.g. "lx_CARS")
    selected_pos: the sfm marker to use for part of speech, or None
    Returns:
        [{"lexeme": "...", "pos": "..."}]
    Citation-form marker (lc / lc_CARS etc.) overrides the lexeme field when present.
    '''
    citation_sfm = 'lc' + selected_lx[2:]  # lx → lc, lx_CARS → lc_CARS

    result = []
    for entry in entries:
        sfm_dict = {}
        for sfm, val in entry:
            sfm_dict[sfm] = val

        lexeme = sfm_dict.get(citation_sfm) or sfm_dict.get(selected_lx, '')
        lexeme = lexeme.strip()
        if not lexeme:
            continue

        pos = sfm_dict.get(selected_pos, '').strip() if selected_pos else ''
        result.append({'lexeme': lexeme, 'pos': pos})

    return result
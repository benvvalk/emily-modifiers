# Emily's Symbol Dictionary
import re

# define your starters here
uniqueEnders = ["LTZ"]

# select the fingerspelling dictionary, i use magnum, but expect most others to use plover
spellingMethod = "magnum"

LONGEST_KEY = 1

# fingerspelling dictionary entries for relevant theories 
spelling = {
        "magnum": {
            "A"       : "a",
            "PW"      : "b",
            "KR"      : "c",
            "TK"      : "d",
            "E"       : "e",
            "TP"      : "f",
            "TKPW"    : "g",
            "H"       : "h",
            "AOEU"    : "i",
            "SKWRAEU" : "j",
            "K"       : "k",
            "HR"      : "l",
            "PH"      : "m",
            "TPH"     : "n",
            "O"       : "o",
            "P"       : "p",
            "KW"      : "q",
            "R"       : "r",
            "S"       : "s",
            "T"       : "t",
            "U"       : "u",
            "SR"      : "v",
            "W"       : "w",
            "KP"      : "x",
            "KWR"     : "y",
            "STKPWHR" : "z",
            },
        "plover": {
            "A"     : "a",
            "PW"    : "b",
            "KR"    : "c",
            "TK"    : "d",
            "E"     : "e",
            "TP"    : "f",
            "TKPW"  : "g",
            "H"     : "h",
            "EU"    : "i",
            "SKWR"  : "j",
            "K"     : "k",
            "HR"    : "l",
            "PH"    : "m",
            "TPH"   : "n",
            "O"     : "o",
            "P"     : "p",
            "KW"    : "q",
            "R"     : "r",
            "S"     : "s",
            "T"     : "t",
            "U"     : "u",
            "SR"    : "v",
            "W"     : "w",
            "KP"    : "x",
            "KWR"   : "y",
            "STKPW" : "z",
            }
        }

# same as emily-symbols format, but mirrored for use on the left hand
symbols = {
        "KH"    : ["tab", "backspace", "delete", "escape"],
        "KPWR"  : ["up", "left", "right", "down"],
        "KPWHR" : ["pageup}", "home", "end", "pagedown}"],
        ""      : ["", "return", "tab", "space"],

        # typable symbols
        "HR"     : ["exclam", "notsign", "", "exclamdown"],
        "WH"     : ["quotedbl", "", "", ""],
        "TKHR"   : ["numbersign", "copyright", "registered", ""],
        "TPWR"   : ["dollar", "yen", "euro", "sterling"],
        "PWHR"   : ["percent", "", "", ""],
        "PWH"    : ["ampersand", "", "", ""],
        "H"      : ["apostrophe", "", "", ""],
        "TPH"    : ["parenleft", "bracketleft", "less", "braceleft"],
        "KWR"    : ["parenright", "bracketright", "greater", "braceright"],
        "T"      : ["asterisk", "", "section", "multiply"],
        "K"      : ["plus", "", "paragraph", "plusminus"],
        "W"      : ["comma", "", "", ""],
        "TP"     : ["minus", "", "", ""],
        "R"      : ["period", "", "periodcentered", ""],
        "PR"     : ["slash", "", "", "division"],
        "TK"     : ["colon", "", "", ""],
        "WR"     : ["semicolon", "", "", ""],
        "TKPW"   : ["equal", "", "", ""],
        "PWL"    : ["question", "questiondown", "", ""],
        "TKPWHR" : ["at", "", "", ""],
        "WH"     : ["backslash", "", "", ""],
        "KPR"    : ["asciicircum", "guillemotright", "guillemotleft", "degree"],
        "KW"     : ["underscore", "", "", "mu"],
        "P"      : ["grave", "", "", ""],
        "PW"     : ["bar", "", "", "brokenbar"],
        "KPWH"   : ["asciitilde", "", "", ""]
}

def lookup(chord):

    # extract the chord for easy use
    stroke = chord[0]

    # quick tests to avoid regex if non-relevant stroke is sent
    if len(chord) != 1:
        raise KeyError
    assert len(chord) <= LONGEST_KEY

    # extract relevant parts of the stroke
    firstMatch = re.fullmatch(r'([#STKPWHR]*)([AO]*)([*-]*)([EU]*)([FRPB]*)([LGTSDZ]*)', stroke)

    # error out if there are no matches found
    if firstMatch is None:
        raise KeyError
    # name the relevant extracted parts of the regex
    (key, vowel1, seperator, vowel2, modifiers, ender) = firstMatch.groups()

    # if the user doesn't specify a modifier, then error out as the dictionary has no use otherwise
    if modifiers is None:
        raise KeyError

    # combine the relevant parts of the stroke into a nice name
    pattern = key + vowel1 + vowel2

    if ender not in uniqueEnders:
        raise KeyError

    # use * to distinguish symbol input from numerical or character input
    if "*" in seperator:
        # symbol input
        # extract the part of the symbol input
        secondMatch = re.fullmatch(r'([STKPWHR]*)([AO]*)([EU]*)', pattern)
        # into variables
        (pattern, variants, vowel2) = secondMatch.groups()
        # if the pattern is not recognised, error out
        if pattern not in symbols:
           raise KeyError

        # calculate the variant count
        variant = 0
        if 'O' in variants:
            variant = variant + 1
        if 'A' in variants:
            variant = variant + 2

        # get the entry 
        entry = symbols[pattern]
        if type(entry) == list:
            extract = entry[variant]
            # error out if the entry isn't applicable
            if extract == "":
                return KeyError

            character = extract
        else:
            character = entry
    else:
        # numbers or letters
        # extract relevant parts of the stroke
        secondMatch = re.fullmatch(r'([STKPWHR]*)([AO]*)([-EU]*)', pattern)
        (shape, number, vowel2) = secondMatch.groups()

        # AO is unused in finger spelling, thus used to disginguish numerical input
        if number == ("AO"):

            # left-hand bottom row conuts in binary for numbers 0-9
            count = 0
            if "R" in shape:
                count = count + 1
            if "W" in shape:
                count = count + 2
            if "K" in shape:
                count = count + 4
            if "S" in shape:
                count = count + 8

            # if KP is being held as well, then user is inputting a Fx key - like alt+F4
            function = False
            if "T" in shape and "P" in shape:
                function = True

            # add the 'F' if F number
            if function:
                character = "F" + str(count)
                if count > 12:
                    raise KeyError
            else:
                if count > 9:
                    raise KeyError
                character = str(count)
        else:
            # finger spelling input
            entry = pattern + number + vowel2

            # check for entry in dictionary 
            if entry not in spelling[spellingMethod]:
                raise KeyError
            character = spelling[spellingMethod][pattern+number+vowel2]

    # accumulate list of modifiers to be added to the character
    # may need to reorder?
    modKeys = modifiers
    mods = []
    if "R" in modKeys:
        mods.append("shift")
    if "F" in modKeys:
        mods.append("control")
    if "B" in modKeys:
        mods.append("alt")
    if "P" in modKeys:
        mods.append("super")

    # apply those modifiers
    combo = character
    for mod in mods:
        combo = mod + "(" + combo + ")"

    # package it up with the syntax
    ret = "{#" + combo + "}"

    # all done! :D
    return ret
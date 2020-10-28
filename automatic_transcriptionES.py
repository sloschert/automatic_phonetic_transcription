"""
This command line programm turns any Spanish word into it's phonetic
transcription in X-Sampa.
"""

import re
import sys
import pyperclip

if len(sys.argv) == 1:
    originalPron = pyperclip.paste()
elif len(sys.argv) == 2:
    originalPron = sys.argv[1]
else:
    print("Warning: Max. one command-line argument will be taken into \
    consideration.")
    originalPron = sys.argv[1]

pron = originalPron
stress = None

# pseudonyms: j\ = ä; tS = ö


def create_pron_list():
    """
    create pron list
    """
    global pronList
    pronList = []
    for x in range(len(pron)):
        pronList.append(pron[x])
    return pronList


def createConsAndVocCode():
    """
    create consonants and vocals code
    """
    global consAndVocCode
    consAndVocCode = []
    for i in range(len(pron)):
        if pron[i] in consList:
            consAndVocCode.append("c")
        elif pron[i] in vocList:
            consAndVocCode.append("v")
        else:
            consAndVocCode.append("x")
    consAndVocCode = "".join(consAndVocCode)
    return consAndVocCode


def insertDotAtPosition(insertPoint):
    """
    inserts dots at specified position
    """
    global pron
    global pronList
    if len(pronList) >= insertPoint + 2:
        pronList.insert(insertPoint, ".")
        pron = "".join(pronList)
        return pron


def endsOnVowelEtc(string):
    """
    checks if string ends on vowel, n or s
    """
    # vowelEtcList = [a, e, u, o, i, n, s]
    x = re.findall("a$|e$|u$|o$|n$|i$|s$", string)
    return bool(x)


def findNearestDot(possibleStress, list):
    """
    finds the nearest dot
    """
    # print("original list: ", list)
    ergebnisSubtraktion = []
    z = 0
    while z < len(list):
        e = abs(possibleStress - list[z])
        ergebnisSubtraktion.append(e)
        z += 1
    # print("result subtraction: ", ergebnisSubtraktion)
    # print("smallest number: ", min(ergebnisSubtraktion))
    listPositionNearestDot = \
        ergebnisSubtraktion.index(min(ergebnisSubtraktion))
    return list[listPositionNearestDot]


def fricativesChangePos(f1, f2, string):
    """
    changes position of fricatives
    """
    string = string.replace(f1 + "." + f2, "." + f1 + f2)
    return string


pron = pron.lower().replace(" ", "")

if pron.find("h") == 0:
    pron = pron.replace("h", "", 1)

if pron.find("á") != -1:
    stress = pron.find("á")
    pron = pron.replace("á", "a")
if pron.find("í") != -1:
    stress = pron.find("í")
    pron = pron.replace("í", "i")
if pron.find("ú") != -1:
    stress = pron.find("ú")
    pron = pron.replace("ú", "u")
if pron.find("ó") != -1:
    stress = pron.find("ó")
    pron = pron.replace("ó", "o")
if pron.find("é") != -1:
    stress = pron.find("é")
    pron = pron.replace("é", "e")
pron = pron.replace("ö", "o").replace("ä", "a").replace("oo", "u").\
    replace("nc", "Nc").replace("ng", "Ng").replace("nj", "Nj"). \
    replace("nq", "Nq").replace("x", "ks").replace("ph", "f").\
    replace("ll", "L").replace("qu", "k").replace("i̯", "j").\
    replace("ʧ", "tS").replace("r", "4").replace("44", "r")

if pron.find("4") == 0:
    pron = pron.replace("4", "r", 1)

pron = pron.replace("ge", "xe").replace("gi", "xi").replace("gui", "gi").\
        replace("gue", "ge").replace("ɣ", "G").replace("g", "G")
if pron.find("G") == 0:
    pron = pron.replace("G", "g", 1)
pron = pron.replace("β", "B").replace("ð", "D").replace("n̩", "n").\
    replace("ṇ", "n").replace("np", "mp").replace("nb", "mb").\
    replace("nk", "Nk").replace("NG", "Ng").replace("NGe", "Nge").\
    replace("θ", "T").replace("ʎ", "L").replace("ˠ", "k")
pron = pron.replace("ɟ", "ä")       # ɟ --> j\ --> ä
pron = pron.replace("ɲ", "J").replace("ñ", "J").replace("ŋ", "N").\
    replace("u̯", "w").replace("j", "x").replace("v", "B").replace("b", "B")
if pron.find("B") == 0:
    pron = pron.replace("B", "b", 1)
pron = pron.replace("d", "D")
if pron.find("D") == 0:
    pron = pron.replace("D", "d", 1)

pron = pron.replace("ch", "tS").replace("sh", "S").replace("z", "T").\
    replace("ci", "Ti").replace("ce", "Te").replace("c", "k").\
    replace("nD", "nd").replace("mD", "md").replace("lD", "ld")
pron = re.sub("y$", "j", pron)      # y at end of pron --> j
pron = pron.replace("y", "ä")       # y --> j\ -- ä
pron = pron.replace("tS", "ö")      # tS --> ö

consList = ["4", "b", "B", "d", "D", "f", "g", "G", "k", "l", "L", "m", "n",
            "J", "ä", "ö", "N", "p", "r", "s", "t", "S", "x", "T", "v", "r"]
vocList = ["a", "e", "i", "o", "u", "@", "E", "O", "j", "w"]
pronList = []
listOfSyllParts = []

# SYLLABLES / DOTS
for j in range(len(originalPron)):
    createConsAndVocCode()
    create_pron_list()

    if re.search("^ccvcv", consAndVocCode)\
            or re.search("^cvcc", consAndVocCode)\
            or re.search("^cvvcv", consAndVocCode):
        insertDotAtPosition(3)
        # e.g. presentacion / discapacitado / biologo
    elif re.search("^ccvccv", consAndVocCode)\
            or re.search("^cvvcc", consAndVocCode)\
            or re.search("^ccvv", consAndVocCode):
        insertDotAtPosition(4)
        # e.g. grande / fuente / krej
    elif re.search("^ccvccc", consAndVocCode):
        insertDotAtPosition(5)
        # e.g. transcripcion
    elif re.search("^cvcv", consAndVocCode)\
            or re.search("^vcc", consAndVocCode)\
            or re.search("^vvc", consAndVocCode):
        insertDotAtPosition(2)
        # e.g. pacitado / imposible / aire
    elif re.search("^vcv", consAndVocCode):
        insertDotAtPosition(1)
        # e.g. identificacion

    listOfSyllables = re.split(r"\.", pron)
    listOfSyllParts.append(listOfSyllables[0])

    if len(listOfSyllables) > 1:
        pron = listOfSyllables[1]
    else:
        pron = ".".join(listOfSyllParts)
        break

pron = "." + pron   # add dot at first position, important for findNearestDot()

pron = fricativesChangePos("k", "l", pron)
pron = fricativesChangePos("t", "4", pron)
pron = fricativesChangePos("f", "4", pron)
pron = fricativesChangePos("B", "l", pron)
pron = fricativesChangePos("b", "l", pron)
pron = fricativesChangePos("p", "l", pron)
pron = fricativesChangePos("b", "4", pron)
pron = fricativesChangePos("B", "4", pron)
pron = fricativesChangePos("f", "l", pron)
pron = fricativesChangePos("D", "4", pron)
pron = fricativesChangePos("d", "4", pron)
pron = fricativesChangePos("g", "4", pron)
pron = fricativesChangePos("G", "4", pron)
pron = fricativesChangePos("p", "4", pron)
pron = fricativesChangePos("k", "l", pron)

# diptongos
pron = pron.replace("io", "jo").replace("eu", "ew").replace("ie", "je").\
        replace("ia", "ja").replace("ue", "we").replace("ai", "aj"). \
        replace("ua", "wa").replace("au", "aw").replace("ui", "wi")

# /r/ AFTER n, l, S, s
pron = pron.replace("n4", "nr")
pron = pron.replace("l4", "lr")
pron = pron.replace("S4", "Sr")
pron = pron.replace("s4", "zr")

# ; /z/ instead of /s/ BEFORE   l, m, n, B, r, G, D
pron = pron.replace("sl", "zl")
pron = pron.replace("sm", "zm")
pron = pron.replace("sn", "zn")
pron = pron.replace("sB", "zB")
pron = pron.replace("sG", "zG")
pron = pron.replace("sD", "zD")

pron = pron.replace("s.l", "z.l")
pron = pron.replace("s.m", "z.m")
pron = pron.replace("s.n", "z.n")
pron = pron.replace("s.B", "z.B")
pron = pron.replace("s.r", "z.r")
pron = pron.replace("s.G", "z.G")
pron = pron.replace("s.D", "z.D")

# STRESS / ANFUERUNGSZEICHEN
listOfDotsPosition = []
for match in re.finditer(r"\.", pron):       # where are the dots?
    listOfDotsPosition.append(match.start())

# was there a stress? than put stress to possible stress position..
if stress is not None:
    possibleStressPosition = (stress-1) * 1.5
    # print("possible stress position ", possibleStressPosition)
    nearestDot = findNearestDot(possibleStressPosition, listOfDotsPosition)
    # print("nearest Dot: ", nearestDot)
    pron = pron[:nearestDot] + ".\"" + pron[nearestDot+1:]
else:
    if len(listOfDotsPosition) > 0:
        positionLastDot = listOfDotsPosition[len(listOfDotsPosition) - 1]
        positionForelastDot = listOfDotsPosition[len(listOfDotsPosition) - 2]
        if len(listOfDotsPosition) > 1:
            if endsOnVowelEtc(pron):
                pron = pron[:positionForelastDot] + ".\"" + \
                    pron[positionForelastDot+1:]
            else:
                pron = pron[:positionLastDot] + ".\"" + \
                    pron[positionLastDot+1:]
        elif len(listOfDotsPosition) == 1:
            if endsOnVowelEtc(pron):
                pron = "\"" + pron
            else:
                pron = pron[:positionLastDot] + ".\"" +\
                    pron[positionLastDot + 1:]
    else:
        print("-- Pron has only one Syllable --")

# last operations
pron = pron.replace(".", "", 1)     # delete first dot again
pron = create_pron_list()
pron = " ".join(pron)               # put spaces
pron = pron.replace("ä", "j\\")
pron = pron.replace("ö", "tS")

print("\nold: ", originalPron)
print("new: ", pron)

pyperclip.copy(pron)

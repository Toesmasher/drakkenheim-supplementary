#!/usr/bin/env python

import argparse
import os
import os.path
import shutil
import subprocess

# Parse and validate arguments
parser = argparse.ArgumentParser("Drakkenheim Art Extractor")
parser.add_argument("--pdf", type = str, required = True, help = "Path to the Drakkenheim PDF")
args = parser.parse_args()

SCRIPTPATH = os.path.realpath(__file__)
SCRIPTDIR = os.path.dirname(SCRIPTPATH)

# Ensure poppler and imagemagick is installed and available
tool_pdfimages = shutil.which("pdfimages")
tool_convert = shutil.which("convert")

if not tool_pdfimages:
    print("pdfimages not found in $PATH, install it via your package manager")
    print("Relevant package: poppler")
    exit(-1)
elif not tool_convert:
    print("convert not found in $PATH, install it via your package manager")
    print("Relevant packages: ImageMagick")
    exit(-1)

type_humanoids = "Humanoids"
type_monsters = "Monsters"
type_visualaids = "VisualAids"
images = [
    # Name of image, output directory, page number, image number, masked
    # Humanoids
    [ "AA-EldrickRuneweaver", type_humanoids, 28, 14, True ],
    [ "AA-River", type_humanoids, 31, 9, True],

    [ "FF-LucretiaMathias", type_humanoids, 34, 17, True ],
    [ "FF-NathanielFlint", type_humanoids, 36, 4, True ],
    [ "FF-NathanielFlint2", type_humanoids, 96, 12, True ],

    [ "HL-EliasDrexel", type_humanoids, 40, 12, True ],
    [ "HL-TheMasterOfTheForge", type_humanoids, 42, 7, True ],
    [ "HL-TheApothecary", type_humanoids, 45, 4, True ],

    [ "SO-TheodoreMarshal", type_humanoids, 46, 11, True ],
    [ "SO-CassandraWyatt", type_humanoids, 49, 7, True ],
    [ "SO-OpheliaReed", type_humanoids, 50, 7, True ],
    [ "SO-PyrePriest", type_humanoids, 161, 7, True ],

    [ "QM-TheQueenOfThieves", type_humanoids, 52, 9, True ],
    [ "QM-Innkeeper", type_humanoids, 87, 7, True ],
    [ "QM-GenericThief", type_humanoids, 167, 4, True ],

    [ "Misc-GerthrudeIronhelm", type_humanoids, 112, 7, True ],
    [ "Misc-RyanGreymere", type_humanoids, 145, 4, True ],
    [ "Misc-DeleriumMage", type_humanoids, 199, 4, True ],

    [ "ApxB-Cavalier", type_humanoids, 222, 4, True ],
    [ "ApxB-Chaplain", type_humanoids, 222, 12, True ],
    [ "ApxB-HedgeMage", type_humanoids, 223, 7, True ],
    [ "ApxB-Scoundrel", type_humanoids, 223, 9, True ],

    # Monsters
    [ "LivingDeepHaze", type_monsters, 32, 7, True ],
    [ "CraterWurm", type_monsters, 126, 1, True ],
    [ "HazeHulkHunter", type_monsters, 131, 9, True ],
    [ "QueenLenore", type_monsters, 142, 4, True ],
    [ "BigLinda", type_monsters, 166, 1, True ],
    [ "Amalgamation", type_monsters, 182, 1, True ],
    [ "TheQueensRetinue", type_monsters, 201, 4, True ],
    [ "WarpWitch", type_monsters, 202, 4, True ],
    [ "DeleriumDregKnight", type_monsters, 203, 7, True ],
    [ "HazeHulk", type_monsters, 204, 10, True ],
    [ "ProteanAbomination", type_monsters, 205, 10, True ],
    [ "Ratling", type_monsters, 206, 13, True ],
    [ "AnimatedDeleriumSludge", type_monsters, 207, 7, True ],
    [ "EntropicFlame", type_monsters, 208, 13, True ],
    [ "HypnoticEldritchBlossom", type_monsters, 209, 14, True ],
    [ "CrimsonCountess", type_monsters, 212, 12, True ],
    [ "Executioner", type_monsters, 213, 10, True ],
    [ "LordOfTheFeast", type_monsters, 215, 12, True ],
    [ "PaleMan", type_monsters, 216, 10, True ],
    [ "RatPrince", type_monsters, 217, 15, True ],

    # Visual Aids
    [ "DrakkenheimMapTop", type_visualaids, 2, 0, False ],
    [ "DrakkenheimMapBottom", type_visualaids, 3, 0, False ],
    [ "TakingTheSacrament", type_visualaids, 37, 1, True ],
    [ "CathedralSermon", type_visualaids, 51, 4, False ],
    [ "RobbedFallingFire", type_visualaids, 59, 4, False ],
    [ "EmberwoodVillage", type_visualaids, 60, 1, True ],
    [ "WagonToEmberwood", type_visualaids, 65, 1, True ],
    [ "MutatingGuy", type_visualaids, 68, 1, True ],
    [ "ExploringTheRuins", type_visualaids, 73, 1, True ],
    [ "DrakkenheimInnerWalls", type_visualaids, 76, 1, True ],
    [ "DrakkenheimOuterWalls", type_visualaids, 77, 1, True ],
    [ "DrakkenheimOuterWalls2", type_visualaids, 78, 1, True ],
    [ "BlackIvoryInn", type_visualaids, 79, 1, True ],
    [ "BuckledownRow", type_visualaids, 84, 1, True ],
    [ "BuckledownArena", type_visualaids, 89, 4, False ],
    [ "ChapelOfSaintBrenna", type_visualaids, 90, 4, True ], # A fun inconsistent 4 for a top image
    [ "CathedralCorruption", type_visualaids, 94, 7, False ],
    [ "EckermanMill", type_visualaids, 97, 2, True ], # And a fun inconsistent 2
    [ "ExploringTheRuins2", type_visualaids, 98, 1, True ],
    [ "ReedManor", type_visualaids, 102, 1, True ],
    [ "OscarYorensLab", type_visualaids, 107, 4, False ],
    [ "ShrineOfMorrigan", type_visualaids, 108, 1, True ], # Full page, but still masked...
    [ "SmithyOnTheScar", type_visualaids, 110, 1, True ],
    [ "SticksFerry", type_visualaids, 115, 1, True ],
    [ "Gargoyles", type_visualaids, 116, 1, True ],
    [ "GarmyrTempleGate", type_visualaids, 120, 1, True ],
    [ "CosmologicalClocktower", type_visualaids, 122, 1, True ],
    [ "KleinbergEstate", type_visualaids, 130, 1, True ],
    [ "OldTownCistern", type_visualaids, 135, 1, True ],
    [ "RoseTheatre", type_visualaids, 144, 1, True ],
    [ "SaintVitruviosCathedral", type_visualaids, 147, 1, True ],
    [ "MutatedBoy", type_visualaids, 148, 4, False ],
    [ "CathedralCatacombs", type_visualaids, 151, 1, True ],
    [ "ExecutionerEncounter", type_visualaids, 157, 4, False ],
    [ "CampDawn", type_visualaids, 158, 1, True ],
    [ "CampDawn2", type_visualaids, 159, 1, True ],
    [ "CourtOfThieves", type_visualaids, 162, 1, True ],
    [ "DrakkenheimGarrison", type_visualaids, 168, 1, True ],
    [ "InscrutableTower", type_visualaids, 173, 4, False ],
    [ "SaintSelinasMonastery", type_visualaids, 179, 1, True ],
    [ "PlayersReeeeeallyScrewedUp", type_visualaids, 191, 1, True ],
    [ "Drakkenforce", type_visualaids, 196, 1, True ],
    [ "RandomEncounter-Dregs", type_visualaids, 200, 1, True ],
    [ "HoodedLantersPlanning", type_visualaids, 218, 2, True ],
    [ "LucretiaMathias", type_visualaids, 220, 1, True ],
    [ "QueenOfThieves", type_visualaids, 221, 4, True ],
    [ "AldorTheImmense", type_visualaids, 225, 1, True ], # Weird one, could just be copied
    [ "MapOfWestemar", type_visualaids, 243, 1, True ],
]

tmpname = "/tmp/drakkenheim"
tool_pdfimages_imgtype = "-png"
for i in images:
    name = i[0]
    dir = i[1]
    page = i[2]
    image = i[3]
    masked = i[4]

    dirname = os.path.join(SCRIPTDIR, dir)
    finalname = os.path.join(dirname, "%s.png" % (name))
    imagename = os.path.join(SCRIPTDIR, "%s-%03i.png" % (tmpname, image))
    maskname = os.path.join(SCRIPTDIR, "%s-%03i.png" % (tmpname, image + 1))

    if not os.path.isdir(dirname):
        print("Creating directory %s" % dir)
        os.mkdir(dirname)

    print("%s: Extracting from page %i... " % (name, page), end = '', flush = True)
    subprocess.call([ tool_pdfimages, tool_pdfimages_imgtype, "-f", str(page), "-l", str(page),
                      args.pdf, tmpname ])

    if masked:
        print("Masking and finalizing...")
        subprocess.call([ tool_convert, imagename, maskname, "-alpha", "off", "-compose",
                          "copy-opacity", "-composite", finalname])
    else:
        print("Not masked, copying original...")
        shutil.copy(imagename, finalname)

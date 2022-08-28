#!/usr/bin/env python

import argparse
import os
import os.path
import shutil
import subprocess

# Parse and validate arguments
parser = argparse.ArgumentParser("Drakkenheim Art Extractor")
parser.add_argument("--pdf", type = str, required = True, help = "Path to the Drakkenheim PDF")
parser.add_argument("--type", type = str, required = False, help = "Type of image to create",
                    choices=["png", "jpg"], default="png")
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

type_npc = "NPCs"
type_monsters = "Monsters"
type_visualaids = "VisualAids"
images = [
    # Name of image, output directory, page number, image number, masked
    # NPCs
    #[ "AA-EldrickRuneweaver", type_npc, 28, 14, True ],
    #[ "AA-River", type_npc, 31, 9, True],

    #[ "FF-LucretiaMathias", type_npc, 34, 17, True ],
    #[ "FF-NathanielFlint", type_npc, 36, 4, True ],
    #[ "FF-NathanielFlint2", type_npc, 96, 12, True ],

    #[ "HL-EliasDrexel", type_npc, 40, 12, True ],
    #[ "HL-TheMasterOfTheForge", type_npc, 42, 7, True ],
    #[ "HL-TheApothecary", type_npc, 45, 4, True ],

    #[ "SO-TheodoreMarshal", type_npc, 46, 11, True ],
    #[ "SO-CassandraWyatt", type_npc, 49, 7, True ],
    #[ "SO-OpheliaReed", type_npc, 50, 7, True ],

    #[ "QM-TheQueenOfThieves", type_npc, 52, 9, True ],
    #[ "QM-Innkeeper", type_npc, 87, 7, True ],

    #[ "Dwarves-GerthrudeIronhelm", type_npc, 112, 7, True ],

    # Monsters
    #[ "LivingDeepHaze", type_monsters, 32, 7, True ],

    # Visual Aids
    #[ "TakingTheSacrament", type_visualaids, 37, 1, True ],
    #[ "CathedralSermon", type_visualaids, 51, 4, False ],
    #[ "RobbedFallingFire", type_visualaids, 59, 4, False ],
    #[ "EmberwoodVillage", type_visualaids, 60, 1, True ]
    #[ "WagonToEmberwood", type_visualaids, 65, 1, True ],
    #[ "MutatingGuy", type_visualaids, 68, 1, True ],
    #[ "ExploringTheRuins", type_visualaids, 73, 1, True ],
    #[ "DrakkenheimInnerWalls", type_visualaids, 76, 1, True ],
    #[ "DrakkenheimOuterWalls", type_visualaids, 77, 1, True ],
    #[ "DrakkenheimOuterWalls2", type_visualaids, 78, 1, True ],
    #[ "BlackIvoryInn", type_visualaids, 79, 1, True ],
    #[ "BuckledownRow", type_visualaids, 84, 1, True ],
    #[ "BuckledownArena", type_visualaids, 89, 4, False ],
    #[ "ChapelOfSaintBrenna", type_visualaids, 90, 4, True ], # A fun inconsistent 4 for a top image
    #[ "CathedralCorruption", type_visualaids, 94, 4, False ],
    #[ "EckermanMill", type_visualaids, 97, 2, True ], # And a fun inconsistent 2
    #[ "ExploringTheRuins2", type_visualaids, 98, 1, True ],
    #[ "ReedManor", type_visualaids, 102, 1, True ],
    #[ "OscarYorensLab", type_visualaids, 107, 4, False ],
    #[ "ShrineOfMorrigan", type_visualaids, 108, 1, True ], # Full page, but still masked...
    #[ "SmithyOnTheScar", type_visualaids, 110, 1, True ],
]

tmpname = "/tmp/drakkenheim"
tool_pdfimages_imgtype = "-j" if args.type == "jpg" else "-png"
for i in images:
    name = i[0]
    dir = i[1]
    page = i[2]
    image = i[3]
    masked = i[4]

    dirname = os.path.join(SCRIPTDIR, dir)
    finalname = os.path.join(dirname, "%s.%s" % (name, args.type))
    imagename = os.path.join(SCRIPTDIR, "%s-%03i.%s" % (tmpname, image, args.type))
    maskname = os.path.join(SCRIPTDIR, "%s-%03i.%s" % (tmpname, image + 1, args.type))

    if not os.path.isdir(dirname):
        print("Creating directory %s" % dirname)
        os.mkdir(dirname)

    print("%s: Extracting from page %i... " % (name, page), end = '', flush = True)
    subprocess.call([ tool_pdfimages, tool_pdfimages_imgtype, "-f", str(page), "-l", str(page),
                      args.pdf, tmpname ])

    if image == 0:
        print("Aborting")
        break

    if masked:
        print("Masking and finalizing...")
        subprocess.call([ tool_convert, imagename, maskname, "-alpha", "off", "-compose",
                          "copy-opacity", "-composite", finalname])
    else:
        print("Not masked, copying original...")
        shutil.copy(imagename, finalname)

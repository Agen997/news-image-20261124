# A working news-image entry (Python 3.13, standard library only): its image
# is the entry.png beside this file, and the program copies it to
# /output/entry.png. The gate takes a whole PNG or JPEG of at most 1 MiB
# and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
#
# The image itself is drawn by draw.py (run it to regenerate entry.png):
# a newspaper front page for Tuesday 24 November 2026 — masthead with the
# date, the Huawei verdict as the lead, Ukraine's strikes on Russian ships,
# NATO's space warning, the US losing measles-free status, Sanofi's $41bn
# Insmed deal, the Turkish helicopter crash, plus markets and sport.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")

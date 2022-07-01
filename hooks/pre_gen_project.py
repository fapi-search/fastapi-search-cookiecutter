import os
import sys

have_poetry = os.system("poetry -V") == 0
if not have_poetry:
    print("Couldn't find poetry, please install, see: https://python-poetry.org/")
    sys.exit(1)

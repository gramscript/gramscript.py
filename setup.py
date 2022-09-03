

import re
from sys import argv

from setuptools import setup

from compiler.api import compiler as api_compiler
from compiler.error import compiler as error_compiler

# from compiler.docs import compiler as docs_compiler

if len(argv) > 1 and argv[1] != "sdist":
    api_compiler.start()
    error_compiler.start()
    # docs_compiler.start()

# PyPI doesn't like raw html
with open("README.rst", encoding="UTF-8") as f:
    readme = re.sub(r"\.\. \|.+\| raw:: html(?:\s{4}.+)+\n\n", "", f.read())
    readme = re.sub(
        r"\|header\|", "|logo|\n\n|description|\n\n|scheme| |mtproto|", readme)

setup(long_description=readme)

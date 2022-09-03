from compiler.error import compiler as error_compiler
from compiler.docs import compiler as docs_compiler
from compiler.api import compiler as api_compiler
from setuptools import setup, find_packages, Command
from sys import argv
import shutil
import re
import os
# MIT License

# Copyright (c) 2022 Gramscript Telegram API

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

with open("gramscript/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()


class Clean(Command):
    DIST = ["./build", "./dist", "./gramscript.egg-info"]
    API = [
        "gramscript/errors/exceptions", "gramscript/raw/functions", "gramscript/raw/types", "gramscript/raw/base",
        "gramscript/raw/all.py"
    ]
    DOCS = [
        "docs/source/telegram", "docs/build", "docs/source/api/methods", "docs/source/api/types",
        "docs/source/api/bound-methods"
    ]

    ALL = DIST + API + DOCS

    description = "Clean generated files"

    user_options = [
        ("dist", None, "Clean distribution files"),
        ("api", None, "Clean generated API files"),
        ("docs", None, "Clean generated docs files"),
        ("all", None, "Clean all generated files"),
    ]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)

        self.dist = None
        self.api = None
        self.docs = None
        self.all = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        paths = set()

        if self.dist:
            paths.update(Clean.DIST)

        if self.api:
            paths.update(Clean.API)

        if self.docs:
            paths.update(Clean.DOCS)

        if self.all or not paths:
            paths.update(Clean.ALL)

        for path in sorted(list(paths)):
            try:
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            except OSError:
                print(f"skipping {path}")
            else:
                print(f"removing {path}")


class Generate(Command):
    description = "Generate gramscript files"

    user_options = [
        ("api", None, "Generate API files"),
        ("docs", None, "Generate docs files")
    ]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)

        self.api = None
        self.docs = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if self.api:
            error_compiler.start()
            api_compiler.start()

        if self.docs:
            docs_compiler.start()


if len(argv) > 1 and argv[1] in ["bdist_wheel", "install", "develop"]:
    api_compiler.start()
    error_compiler.start()

setup(
    name="gramscript",
    version=version,
    description="Telegram MTProto API Client Library and Framework for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/gramscript",
    download_url="https://github.com/gramscript/gramscript/releases/latest",
    author="Dan",
    author_email="dan@gramscript.org",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    keywords="telegram chat messenger mtproto api client library python",
    project_urls={
        "Tracker": "https://github.com/gramscript/gramscript/issues",
        "Community": "https://t.me/gramscript",
        "Source": "https://github.com/gramscript/gramscript",
        "Documentation": "https://docs.gramscript.org",
    },
    python_requires="~=3.6",
    packages=find_packages(exclude=["compiler*"]),
    package_data={
        "gramscript": ["mime.types"],
        "gramscript.storage": ["schema.sql"]
    },
    zip_safe=False,
    install_requires=requires,
    cmdclass={
        "clean": Clean,
        "generate": Generate
    }
)

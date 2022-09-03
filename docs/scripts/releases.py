import requests
import pypandoc
from pathlib import Path
from datetime import datetime
import shutil
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


URL = "https://api.github.com/repos/gramscript/gramscript/releases"
DEST = Path("../source/releases")
INTRO = """
Release Notes
=============

Release notes for gramscript releases will describe what's new in each version, and will also make you aware of any
backwards-incompatible changes made in that version.

When upgrading to a new version of gramscript, you will need to check all the breaking changes in order to find
incompatible code in your application, but also to take advantage of new features and improvements.

**Contents**

""".lstrip("\n")

shutil.rmtree(DEST, ignore_errors=True)
DEST.mkdir(parents=True)

releases = requests.get(URL).json()

with open(DEST / "index.rst", "w") as index:
    index.write(INTRO)

    tags = []

    for release in releases:
        tag = release["tag_name"]
        title = release["name"]
        name = title.split(" - ")[1]

        date = datetime.strptime(
            release["published_at"],
            "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%b %d, %Y")

        body = pypandoc.convert_text(
            release["body"].replace(r"\r\n", "\n"),
            "rst",
            format="markdown_github",
            extra_args=["--wrap=none"]
        )

        tarball_url = release["tarball_url"]
        zipball_url = release["zipball_url"]

        index.write("- :doc:`{} <{}>`\n".format(title, tag))
        tags.append(tag)

        with open(DEST / "{}.rst".format(tag), "w") as page:
            page.write("gramscript " + tag + "\n" +
                       "=" * (len(tag) + 9) + "\n\n")
            page.write("\t\tReleased on " + str(date) + "\n\n")
            page.write(
                "- :download:`Source Code (zip) <{}>`\n".format(zipball_url))
            page.write(
                "- :download:`Source Code (tar.gz) <{}>`\n\n".format(tarball_url))
            page.write(name + "\n" + "-" * len(name) + "\n\n")
            page.write(body + "\n\n")

    index.write("\n.. toctree::\n    :hidden:\n\n")
    index.write("\n".join("    {}".format(tag) for tag in tags))

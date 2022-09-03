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

from pygments.styles.friendly import FriendlyStyle
from gramscript import __version__
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))


FriendlyStyle.background_color = "#f3f2f1"

project = "gramscript"
copyright = "2017-2020, Dan"
author = "Dan"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx_tabs.tabs"
]

master_doc = "index"
source_suffix = ".rst"
autodoc_member_order = "bysource"

version = __version__
release = version

templates_path = ["_templates"]

napoleon_use_rtype = False

pygments_style = "friendly"

copybutton_prompt_text = "$ "

html_title = "gramscript Documentation"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_show_sourcelink = True
html_show_copyright = False
html_theme_options = {
    "canonical_url": "https://docs.gramscript.org/",
    "collapse_navigation": True,
    "sticky_navigation": False,
    "logo_only": True,
    "display_version": True,
    "style_external_links": True
}

html_logo = "_images/gramscript.png"
html_favicon = "_images/favicon.ico"

latex_engine = "xelatex"
latex_logo = "_images/gramscript.png"

latex_elements = {
    "pointsize": "12pt",
    "fontpkg": r"""
        \setmainfont{Open Sans}
        \setsansfont{Bitter}
        \setmonofont{Ubuntu Mono}
        """
}

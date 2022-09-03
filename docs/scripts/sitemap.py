import os
import datetime
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


canonical = "https://docs.gramscript.org/"

dirs = {
    ".": ("weekly", 1.0),
    "intro": ("weekly", 0.9),
    "start": ("weekly", 0.9),
    "api": ("weekly", 0.8),
    "topics": ("weekly", 0.8),
    "releases": ("weekly", 0.8),
    "telegram": ("weekly", 0.6)
}


def now():
    return datetime.datetime.today().strftime("%Y-%m-%d")


with open("sitemap.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    urls = []

    def search(path):
        try:
            for j in os.listdir(path):
                search(f"{path}/{j}")
        except NotADirectoryError:
            if not path.endswith(".rst"):
                return

            path = path.split("/")[1:]

            if path[0].endswith(".rst"):
                folder = "."
            else:
                folder = path[0]

            path = f"{canonical}{'/'.join(path)}"[:-len(".rst")]

            if path.endswith("index"):
                path = path[:-len("index")]

            urls.append((path, now(), *dirs[folder]))

    search("../source")

    urls.sort(key=lambda x: x[3], reverse=True)

    for i in urls:
        f.write(f"    <url>\n")
        f.write(f"        <loc>{i[0]}</loc>\n")
        f.write(f"        <lastmod>{i[1]}</lastmod>\n")
        f.write(f"        <changefreq>{i[2]}</changefreq>\n")
        f.write(f"        <priority>{i[3]}</priority>\n")
        f.write(f"    </url>\n\n")

    f.write("</urlset>")

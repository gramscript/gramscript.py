from typing import NamedTuple, List, Tuple
from pathlib import Path
from functools import partial
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


# from autoflake import fix_code
# from black import format_str, FileMode

HOME_PATH = Path("compiler/api")
DESTINATION_PATH = Path("gramscript/raw")
NOTICE_PATH = "NOTICE"

SECTION_RE = re.compile(r"---(\w+)---")
LAYER_RE = re.compile(r"//\sLAYER\s(\d+)")
COMBINATOR_RE = re.compile(
    r"^([\w.]+)#([0-9a-f]+)\s(?:.*)=\s([\w<>.]+);$", re.MULTILINE)
ARGS_RE = re.compile(r"[^{](\w+):([\w?!.<>#]+)")
FLAGS_RE = re.compile(r"flags\.(\d+)\?")
FLAGS_RE_2 = re.compile(r"flags\.(\d+)\?([\w<>.]+)")
FLAGS_RE_3 = re.compile(r"flags:#")
INT_RE = re.compile(r"int(\d+)")

CORE_TYPES = ["int", "long", "int128", "int256",
              "double", "bytes", "string", "Bool", "true"]

WARNING = """
# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #
""".strip()

# noinspection PyShadowingBuiltins
open = partial(open, encoding="utf-8")

types_to_constructors = {}
types_to_functions = {}
constructors_to_functions = {}
namespaces_to_types = {}
namespaces_to_constructors = {}
namespaces_to_functions = {}


class Combinator(NamedTuple):
    section: str
    qualname: str
    namespace: str
    name: str
    id: str
    has_flags: bool
    args: List[Tuple[str, str]]
    qualtype: str
    typespace: str
    type: str


def snake(s: str):
    # https://stackoverflow.com/q/1175208
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def camel(s: str):
    return "".join([i[0].upper() + i[1:] for i in s.split("_")])


# noinspection PyShadowingBuiltins, PyShadowingNames
def get_type_hint(type: str) -> str:
    is_flag = FLAGS_RE.match(type)
    is_core = False

    if is_flag:
        type = type.split("?")[1]

    if type in CORE_TYPES:
        is_core = True

        if type == "long" or "int" in type:
            type = "int"
        elif type == "double":
            type = "float"
        elif type == "string":
            type = "str"
        elif type in ["Bool", "true"]:
            type = "bool"
        else:  # bytes and object
            type = "bytes"

    if type in ["Object", "!X"]:
        return "TLObject"

    if re.match("^vector", type, re.I):
        is_core = True

        sub_type = type.split("<")[1][:-1]
        type = f"List[{get_type_hint(sub_type)}]"

    if is_core:
        return f"Union[None, {type}] = None" if is_flag else type
    else:
        ns, name = type.split(".") if "." in type else ("", type)
        type = f'"raw.base.' + ".".join([ns, name]).strip(".") + '"'

        return f'{type}{" = None" if is_flag else ""}'


def sort_args(args):
    """Put flags at the end"""
    args = args.copy()
    flags = [i for i in args if FLAGS_RE.match(i[1])]

    for i in flags:
        args.remove(i)

    try:
        args.remove(("flags", "#"))
    except ValueError:
        pass

    return args + flags


def remove_whitespaces(source: str) -> str:
    """Remove whitespaces from blank lines"""
    lines = source.split("\n")

    for i, _ in enumerate(lines):
        if re.match(r"^\s+$", lines[i]):
            lines[i] = ""

    return "\n".join(lines)


def get_docstring_arg_type(t: str, is_list: bool = False, is_gramscript_type: bool = False):
    if t in CORE_TYPES:
        if t == "long":
            return "``int`` ``64-bit``"
        elif "int" in t:
            size = INT_RE.match(t)
            return f"``int`` ``{size.group(1)}-bit``" if size else "``int`` ``32-bit``"
        elif t == "double":
            return "``float`` ``64-bit``"
        elif t == "string":
            return "``str``"
        elif t == "true":
            return "``bool``"
        else:
            return f"``{t.lower()}``"
    elif t == "TLObject" or t == "X":
        return "Any object from :obj:`~gramscript.raw.types`"
    elif t == "!X":
        return "Any method from :obj:`~gramscript.raw.functions`"
    elif t.lower().startswith("vector"):
        return "List of " + get_docstring_arg_type(t.split("<", 1)[1][:-1], True)
    else:
        return f":obj:`{t} <gramscript.raw.base.{t}>`"


def get_references(t: str, kind: str):
    if kind == "constructors":
        t = constructors_to_functions.get(t)
    elif kind == "types":
        t = types_to_functions.get(t)
    else:
        raise ValueError("Invalid kind")

    if t:
        return "\n            ".join(
            f"- :obj:`{i} <gramscript.raw.functions.{i}>`"
            for i in t
        ), len(t)

    return None, 0


# noinspection PyShadowingBuiltins
def start(format: bool = False):
    shutil.rmtree(DESTINATION_PATH / "types", ignore_errors=True)
    shutil.rmtree(DESTINATION_PATH / "functions", ignore_errors=True)
    shutil.rmtree(DESTINATION_PATH / "base", ignore_errors=True)

    with open(HOME_PATH / "source/auth_key.tl") as f1, \
            open(HOME_PATH / "source/sys_msgs.tl") as f2, \
            open(HOME_PATH / "source/main_api.tl") as f3:
        schema = (f1.read() + f2.read() + f3.read()).splitlines()

    with open(HOME_PATH / "template/type.txt") as f1, \
            open(HOME_PATH / "template/combinator.txt") as f2:
        type_tmpl = f1.read()
        combinator_tmpl = f2.read()

    with open(NOTICE_PATH, encoding="utf-8") as f:
        notice = []

        for line in f.readlines():
            notice.append(f"#  {line}".strip())

        notice = "\n".join(notice)

    section = None
    layer = None
    combinators = []

    for line in schema:
        # Check for section changer lines
        section_match = SECTION_RE.match(line)
        if section_match:
            section = section_match.group(1)
            continue

        # Save the layer version
        layer_match = LAYER_RE.match(line)
        if layer_match:
            layer = layer_match.group(1)
            continue

        combinator_match = COMBINATOR_RE.match(line)
        if combinator_match:
            # noinspection PyShadowingBuiltins
            qualname, id, qualtype = combinator_match.groups()

            namespace, name = qualname.split(
                ".") if "." in qualname else ("", qualname)
            name = camel(name)
            qualname = ".".join([namespace, name]).lstrip(".")

            typespace, type = qualtype.split(
                ".") if "." in qualtype else ("", qualtype)
            type = camel(type)
            qualtype = ".".join([typespace, type]).lstrip(".")

            # Pingu!
            has_flags = not not FLAGS_RE_3.findall(line)

            args = ARGS_RE.findall(line)

            # Fix arg name being "self" (reserved python keyword)
            for i, item in enumerate(args):
                if item[0] == "self":
                    args[i] = ("is_self", item[1])

            combinator = Combinator(
                section=section,
                qualname=qualname,
                namespace=namespace,
                name=name,
                id=f"0x{id}",
                has_flags=has_flags,
                args=args,
                qualtype=qualtype,
                typespace=typespace,
                type=type
            )

            combinators.append(combinator)

    for c in combinators:
        qualtype = c.qualtype

        if qualtype.startswith("Vector"):
            qualtype = qualtype.split("<")[1][:-1]

        d = types_to_constructors if c.section == "types" else types_to_functions

        if qualtype not in d:
            d[qualtype] = []

        d[qualtype].append(c.qualname)

        if c.section == "types":
            key = c.namespace

            if key not in namespaces_to_types:
                namespaces_to_types[key] = []

            if c.type not in namespaces_to_types[key]:
                namespaces_to_types[key].append(c.type)

    for k, v in types_to_constructors.items():
        for i in v:
            try:
                constructors_to_functions[i] = types_to_functions[k]
            except KeyError:
                pass

    # import json
    # print(json.dumps(namespaces_to_types, indent=2))

    for qualtype in types_to_constructors:
        typespace, type = qualtype.split(
            ".") if "." in qualtype else ("", qualtype)
        dir_path = DESTINATION_PATH / "base" / typespace

        module = type

        if module == "Updates":
            module = "UpdatesT"

        os.makedirs(dir_path, exist_ok=True)

        constructors = sorted(types_to_constructors[qualtype])
        constr_count = len(constructors)
        items = "\n            ".join(
            [f"- :obj:`{c} <gramscript.raw.types.{c}>`" for c in constructors])

        docstring = f"This base type has {constr_count} constructor{'s' if constr_count > 1 else ''} available.\n\n"
        docstring += f"    Constructors:\n        .. hlist::\n            :columns: 2\n\n            {items}"

        references, ref_count = get_references(qualtype, "types")

        if references:
            docstring += f"\n\n    See Also:\n        This object can be returned by " \
                         f"{ref_count} method{'s' if ref_count > 1 else ''}:" \
                         f"\n\n        .. hlist::\n            :columns: 2\n\n            " + references

        with open(dir_path / f"{snake(module)}.py", "w") as f:
            f.write(
                type_tmpl.format(
                    notice=notice,
                    warning=WARNING,
                    docstring=docstring,
                    name=type,
                    qualname=qualtype,
                    types=", ".join([f"raw.types.{c}" for c in constructors])
                )
            )

    for c in combinators:
        sorted_args = sort_args(c.args)

        arguments = (
            (", *, " if c.args else "") +
            (", ".join(
                [f"{i[0]}: {get_type_hint(i[1])}"
                 for i in sorted_args]
            ) if sorted_args else "")
        )

        fields = "\n        ".join(
            [f"self.{i[0]} = {i[0]}  # {i[1]}"
             for i in sorted_args]
        ) if sorted_args else "pass"

        docstring = ""
        docstring_args = []

        for i, arg in enumerate(sorted_args):
            arg_name, arg_type = arg
            is_optional = FLAGS_RE.match(arg_type)
            flag_number = is_optional.group(1) if is_optional else -1
            arg_type = arg_type.split("?")[-1]

            docstring_args.append(
                "{}{}: {}".format(
                    arg_name,
                    " (optional)".format(flag_number) if is_optional else "",
                    get_docstring_arg_type(
                        arg_type, is_gramscript_type=c.namespace == "gramscript")
                )
            )

        if c.section == "types":
            docstring += f"This object is a constructor of the base type :obj:`~gramscript.raw.base.{c.qualtype}`.\n\n"
        else:
            docstring += f"Telegram API method.\n\n"

        docstring += f"    Details:\n        - Layer: ``{layer}``\n        - ID: ``{c.id}``\n\n"

        if docstring_args:
            docstring += "    Parameters:\n        " + \
                "\n        ".join(docstring_args)
        else:
            docstring += "    **No parameters required.**"

        if c.section == "functions":
            docstring += "\n\n    Returns:\n        " + \
                get_docstring_arg_type(c.qualtype)
        else:
            references, count = get_references(c.qualname, "constructors")

            if references:
                docstring += f"\n\n    See Also:\n        This object can be returned by " \
                             f"{count} method{'s' if count > 1 else ''}:" \
                             f"\n\n        .. hlist::\n            :columns: 2\n\n            " + references

        write_types = read_types = "" if c.has_flags else "# No flags\n        "

        for arg_name, arg_type in c.args:
            flag = FLAGS_RE_2.findall(arg_type)

            if arg_name == "flags" and arg_type == "#":
                write_flags = []

                for i in c.args:
                    flag = FLAGS_RE.match(i[1])
                    if flag:
                        write_flags.append(
                            f"flags |= (1 << {flag.group(1)}) if self.{i[0]} is not None else 0")

                write_flags = "\n        ".join([
                    "flags = 0",
                    "\n        ".join(write_flags),
                    "data.write(Int(flags))\n        "
                ])

                write_types += write_flags
                read_types += "flags = Int.read(data)\n        "

                continue

            if flag:
                index, flag_type = flag[0]

                if flag_type == "true":
                    read_types += "\n        "
                    read_types += f"{arg_name} = True if flags & (1 << {index}) else False"
                elif flag_type in CORE_TYPES:
                    write_types += "\n        "
                    write_types += f"if self.{arg_name} is not None:\n            "
                    write_types += f"data.write({flag_type.title()}(self.{arg_name}))\n        "

                    read_types += "\n        "
                    read_types += f"{arg_name} = {flag_type.title()}.read(data) if flags & (1 << {index}) else None"
                elif "vector" in flag_type.lower():
                    sub_type = arg_type.split("<")[1][:-1]

                    write_types += "\n        "
                    write_types += f"if self.{arg_name} is not None:\n            "
                    write_types += "data.write(Vector(self.{}{}))\n        ".format(
                        arg_name, f", {sub_type.title()}" if sub_type in CORE_TYPES else ""
                    )

                    read_types += "\n        "
                    read_types += "{} = TLObject.read(data{}) if flags & (1 << {}) else []\n        ".format(
                        arg_name, f", {sub_type.title()}" if sub_type in CORE_TYPES else "", index
                    )
                else:
                    write_types += "\n        "
                    write_types += f"if self.{arg_name} is not None:\n            "
                    write_types += f"data.write(self.{arg_name}.write())\n        "

                    read_types += "\n        "
                    read_types += f"{arg_name} = TLObject.read(data) if flags & (1 << {index}) else None\n        "
            else:
                if arg_type in CORE_TYPES:
                    write_types += "\n        "
                    write_types += f"data.write({arg_type.title()}(self.{arg_name}))\n        "

                    read_types += "\n        "
                    read_types += f"{arg_name} = {arg_type.title()}.read(data)\n        "
                elif "vector" in arg_type.lower():
                    sub_type = arg_type.split("<")[1][:-1]

                    write_types += "\n        "
                    write_types += "data.write(Vector(self.{}{}))\n        ".format(
                        arg_name, f", {sub_type.title()}" if sub_type in CORE_TYPES else ""
                    )

                    read_types += "\n        "
                    read_types += "{} = TLObject.read(data{})\n        ".format(
                        arg_name, f", {sub_type.title()}" if sub_type in CORE_TYPES else ""
                    )
                else:
                    write_types += "\n        "
                    write_types += f"data.write(self.{arg_name}.write())\n        "

                    read_types += "\n        "
                    read_types += f"{arg_name} = TLObject.read(data)\n        "

        slots = ", ".join([f'"{i[0]}"' for i in sorted_args])
        return_arguments = ", ".join([f"{i[0]}={i[0]}" for i in sorted_args])

        compiled_combinator = combinator_tmpl.format(
            notice=notice,
            warning=WARNING,
            name=c.name,
            docstring=docstring,
            slots=slots,
            id=c.id,
            qualname=f"gramscript.raw.{c.section}.{c.qualname}",
            arguments=arguments,
            fields=fields,
            read_types=read_types,
            write_types=write_types,
            return_arguments=return_arguments
        )

        directory = "types" if c.section == "types" else c.section

        dir_path = DESTINATION_PATH / directory / c.namespace

        os.makedirs(dir_path, exist_ok=True)

        module = c.name

        if module == "Updates":
            module = "UpdatesT"

        with open(dir_path / f"{snake(module)}.py", "w") as f:
            f.write(compiled_combinator)

        d = namespaces_to_constructors if c.section == "types" else namespaces_to_functions

        if c.namespace not in d:
            d[c.namespace] = []

        d[c.namespace].append(c.name)

    for namespace, types in namespaces_to_types.items():
        with open(DESTINATION_PATH / "base" / namespace / "__init__.py", "w") as f:
            f.write(f"{notice}\n\n")
            f.write(f"{WARNING}\n\n")

            for t in types:
                module = t

                if module == "Updates":
                    module = "UpdatesT"

                f.write(f"from .{snake(module)} import {t}\n")

            if not namespace:
                f.write(
                    f"from . import {', '.join(filter(bool, namespaces_to_types))}")

    for namespace, types in namespaces_to_constructors.items():
        with open(DESTINATION_PATH / "types" / namespace / "__init__.py", "w") as f:
            f.write(f"{notice}\n\n")
            f.write(f"{WARNING}\n\n")

            for t in types:
                module = t

                if module == "Updates":
                    module = "UpdatesT"

                f.write(f"from .{snake(module)} import {t}\n")

            if not namespace:
                f.write(
                    f"from . import {', '.join(filter(bool, namespaces_to_constructors))}\n")

    for namespace, types in namespaces_to_functions.items():
        with open(DESTINATION_PATH / "functions" / namespace / "__init__.py", "w") as f:
            f.write(f"{notice}\n\n")
            f.write(f"{WARNING}\n\n")

            for t in types:
                module = t

                if module == "Updates":
                    module = "UpdatesT"

                f.write(f"from .{snake(module)} import {t}\n")

            if not namespace:
                f.write(
                    f"from . import {', '.join(filter(bool, namespaces_to_functions))}")

    with open(DESTINATION_PATH / "all.py", "w", encoding="utf-8") as f:
        f.write(notice + "\n\n")
        f.write(WARNING + "\n\n")
        f.write(f"layer = {layer}\n\n")
        f.write("objects = {")

        for c in combinators:
            f.write(
                f'\n    {c.id}: "gramscript.raw.{c.section}.{c.qualname}",')

        f.write('\n    0xbc799737: "gramscript.raw.core.BoolFalse",')
        f.write('\n    0x997275b5: "gramscript.raw.core.BoolTrue",')
        f.write('\n    0x1cb5c415: "gramscript.raw.core.Vector",')
        f.write('\n    0x73f1f8dc: "gramscript.raw.core.MsgContainer",')
        f.write('\n    0xae500895: "gramscript.raw.core.FutureSalts",')
        f.write('\n    0x0949d9dc: "gramscript.raw.core.FutureSalt",')
        f.write('\n    0x3072cfa1: "gramscript.raw.core.GzipPacked",')
        f.write('\n    0x5bb8e511: "gramscript.raw.core.Message",')

        f.write("\n}\n")


if "__main__" == __name__:
    HOME_PATH = Path(".")
    DESTINATION_PATH = Path("../../gramscript/raw")
    NOTICE_PATH = Path("../../NOTICE")

    start(format=False)

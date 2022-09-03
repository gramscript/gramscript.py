

from importlib import import_module

from .all import objects
from .core.object import Object

for k, v in objects.items():
    path, name = v.rsplit(".", 1)
    Object.all[k] = getattr(import_module("gramscript.api." + path), name)

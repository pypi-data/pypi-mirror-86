from importlib import import_module
from warnings import warn


def load(candidates=["asof20201118"]):
    for asof in candidates:
        try:
            mod = import_module("shukujitsu.%s" % asof)
        except ImportError as e:
            warn(repr(e), category=ImportWarning, stacklevel=2)
        else:
            return mod.RAW_DATA
    else:
        raise RuntimeError("No holidays data is available")

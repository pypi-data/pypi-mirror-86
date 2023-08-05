# Copyright (c) 2016-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/Zlib

import sys
import os
import platform

is_windows = (bool(platform.win32_ver()[0]) or
              (sys.platform in ("win32", "cygwin")) or
              (sys.platform == "cli" and os.name in ("nt", "ce")) or
              (os.name == "java" and
               "windows" in platform.java_ver()[3][0].lower()))
is_linux   = sys.platform.startswith("linux")
is_osx     = (sys.platform == "darwin")
is_android = False
is_posix   = (os.name == "posix")
is_32bit   = (sys.maxsize <= 2**32)

def defined(varname, _getframe=sys._getframe):
    frame = _getframe(1)
    return varname in frame.f_locals or varname in frame.f_globals

del sys, os, platform

if is_windows:
    from ._windows import DLL_PATH, DLL, dlclose, CFUNC
    from ._windows import timeval
elif is_linux:
    from ._linux   import DLL_PATH, DLL, dlclose, CFUNC
    from ._linux   import timeval
elif is_osx:
    from ._osx     import DLL_PATH, DLL, dlclose, CFUNC
    from ._osx     import timeval
else:
    raise ImportError("unsupported platform")

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from ..core.mapdata import mapdata, mpqapi, fixmapdata
from ..core import RegisterCreatePayloadCallback
from .injector.applyInjector import applyInjector
from .inlinecode.ilcprocesstrig import PreprocessInlineCode
from .injector.mainloop import _MainStarter
from .mpqadd import UpdateMPQ
from ..core.eudfunc.trace.tracetool import _GetTraceMap, _ResetTraceMap
from ..localize import _
from ..utils import ep_eprint
import binascii
import os

traceHeader = None
traceMap = []


def getTraceMap():
    global traceMap, traceHeader
    newTraceHeader, newTraceMap = _GetTraceMap()
    if newTraceMap:
        traceHeader = newTraceHeader
        traceMap = list(newTraceMap)
    _ResetTraceMap()


RegisterCreatePayloadCallback(getTraceMap)


def SaveMap(fname, rootf, *, sectorSize=None):
    """Save output map with root function.

    :param fname: Path for output map.
    :param rootf: Main entry function.
    """

    print(_("Saving to {}...").format(fname))
    chkt = mapdata.GetChkTokenized()

    _ResetTraceMap()

    # Add payload
    root = _MainStarter(rootf)
    PreprocessInlineCode(chkt)
    mapdata.UpdateMapData()

    fixmapdata.FixMapData(chkt)
    applyInjector(chkt, root)

    chkt.optimize()
    rawchk = chkt.savechk()
    print("Output scenario.chk : {:.3}MB".format(len(rawchk) / 1000000))
    mw = mpqapi.MPQ()

    if sectorSize is None:
        # Process by modifying existing mpqfile
        try:
            open(fname, "wb").write(mapdata.GetRawFile())
        except PermissionError:
            ep_eprint(
                _("You lacks permission to get access rights for output map"),
                _("Try to turn off antivirus or StarCraft"),
                sep="\n",
            )
        if not mw.Open(fname):
            ep_eprint("Fail to access output map")
    elif isinstance(sectorSize, int):
        if os.path.isfile(fname):
            try:
                os.remove(fname)
            except PermissionError:
                ep_eprint(
                    _("You lacks permission to get access rights for output map"),
                    _("Try to turn off antivirus or StarCraft"),
                    sep="\n",
                )
        if not mw.Create(fname, sectorSize=sectorSize):
            ep_eprint("Fail to access output map")
        for n, f in mapdata.IterListFiles():
            if f and not mw.PutFile(n, f):
                ep_eprint("Fail to export input map data to output map")
    else:
        ep_eprint("sectorSize should be int. ({})".format(sectorSize))

    if not mw.PutFile("staredit\\scenario.chk", rawchk):
        ep_eprint("Fail to add scenario.chk")
    UpdateMPQ(mw)
    if not mw.Compact():
        ep_eprint("Fail to compact MPQ")
    mw.Close()

    if traceMap:
        traceFname = fname + ".epmap"
        print(_("Writing trace file to {}").format(traceFname))
        with open(traceFname, "w", encoding="utf-8") as wf:
            wf.write("H0: %s\n" % binascii.hexlify(traceHeader[0]).decode("ascii"))
            wf.write("H1: %s\n" % binascii.hexlify(traceHeader[1]).decode("ascii"))
            for k, v in traceMap:
                wf.write(" - %08X : %s\n" % (k, v))

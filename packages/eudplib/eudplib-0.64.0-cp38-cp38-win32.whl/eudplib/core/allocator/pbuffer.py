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


from .rlocint import RlocInt_C

from . import constexpr
from eudplib import utils as ut
from eudplib.localize import _


class Payload:
    def __init__(self, data, prttable, orttable):
        self.data = data
        self.prttable = prttable
        self.orttable = orttable


_packerData = {}


class PayloadBuffer:

    """
    Buffer where EUDObject should write to.
    """

    def __init__(self, totlen):
        self._data = bytearray(totlen)
        self._totlen = totlen
        self._prttable = []
        self._orttable = []

    def StartWrite(self, writeaddr):
        self._datastart = writeaddr
        self._datacur = writeaddr

    def EndWrite(self):
        return self._datacur - self._datastart

    def WriteByte(self, number):
        self._data[self._datacur] = number & 0xFF
        self._datacur += 1

    def WriteWord(self, number):
        self._data[self._datacur + 0] = number & 0xFF
        self._data[self._datacur + 1] = (number >> 8) & 0xFF
        self._datacur += 2

    def WriteDword(self, number):
        number = constexpr.Evaluate(number)

        if number.rlocmode:
            ut.ep_assert(
                self._datacur % 4 == 0, _("Non-const dwords must be aligned to 4byte")
            )
            if number.rlocmode == 1:
                self._prttable.append(self._datacur)
            elif number.rlocmode == 4:
                self._orttable.append(self._datacur)
            else:
                raise ut.EPError(_("rlocmode should be 1 or 4"))

        offset = number.offset
        self._data[self._datacur + 0] = offset & 0xFF
        self._data[self._datacur + 1] = (offset >> 8) & 0xFF
        self._data[self._datacur + 2] = (offset >> 16) & 0xFF
        self._data[self._datacur + 3] = (offset >> 24) & 0xFF
        self._datacur += 4

    def WritePack(self, structformat, arglist):
        """
        ======= =======
          Char   Type
        ======= =======
           B     Byte
           H     Word
           I     Dword
        ======= =======
        """

        try:
            _StructPacker(_packerData[structformat], self, arglist)
        except KeyError:
            _packerData[structformat] = CreateStructPackerData(structformat)
            _StructPacker(_packerData[structformat], self, arglist)

    def WriteBytes(self, b):
        """
        Write bytes object to buffer.

        :param b: bytes object to write.
        """
        if not isinstance(b, bytes):
            b = bytes(b)

        self._data[self._datacur : self._datacur + len(b)] = b
        self._datacur += len(b)

    def WriteSpace(self, spacesize):
        self._datacur += spacesize

    # Internally used
    def CreatePayload(self):
        return Payload(self._data, self._prttable, self._orttable)


def CreateStructPackerData(structformat):
    sizedict = {"B": 1, "H": 2, "I": 4}
    sizelist = []
    for s in structformat:
        sizelist.append(sizedict[s])

    return sizelist


def _StructPacker(sizelist, buf, arglist):
    dpos = buf._datacur
    data = buf._data
    prttb = buf._prttable
    orttb = buf._orttable

    for i, arg in enumerate(arglist):
        argsize = sizelist[i]
        ri = constexpr.Evaluate(arg)

        ut.ep_assert(
            ri.rlocmode == 0 or (sizelist[i] == 4 and dpos % 4 == 0),
            _("Cannot write non-const in byte/word/nonalligned dword."),
        )

        if ri.rlocmode == 1:
            prttb.append(dpos)

        elif ri.rlocmode == 4:
            orttb.append(dpos)

        if sizelist[i] == 1:
            data[dpos] = ri.offset & 0xFF

        elif sizelist[i] == 2:
            data[dpos] = ri.offset & 0xFF
            data[dpos + 1] = (ri.offset >> 8) & 0xFF

        else:
            data[dpos] = ri.offset & 0xFF
            data[dpos + 1] = (ri.offset >> 8) & 0xFF
            data[dpos + 2] = (ri.offset >> 16) & 0xFF
            data[dpos + 3] = (ri.offset >> 24) & 0xFF

        dpos += sizelist[i]

    buf._datacur = dpos

#!/usr/bin/python
# -*- coding: utf-8 -*-
# cython: language_level=3

'''
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
'''

from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from cpython.bytes cimport PyBytes_AsString, PyBytes_FromStringAndSize
from cpython.pycapsule cimport PyCapsule_New, PyCapsule_GetPointer
from libc.string cimport memset, memcpy
from libc.stdint cimport uint32_t, uint16_t

from .rlocint cimport RlocInt_C

from . import constexpr
from eudplib import utils as ut
from eudplib.localize import _


class Payload:

    def __init__(self, data, prttable, orttable):
        self.data = data
        self.prttable = prttable
        self.orttable = orttable


_packerData = {}


cdef class PayloadBuffer:

    '''
    Buffer where EUDObject should write to.
    '''

    cdef size_t _totlen
    cdef public size_t _datastart, _datacur
    cdef public unsigned char* _data
    cdef public list _prttable, _orttable

    def __cinit__(self, size_t totlen):
        self._data = <unsigned char*> PyMem_Malloc(totlen)
        self._totlen = totlen
        self._prttable = []
        self._orttable = []

    def __dealloc(self):
        PyMem_Free(self._data)

    cpdef void StartWrite(self, size_t writeaddr):
        self._datastart = writeaddr
        self._datacur = writeaddr

    cpdef size_t EndWrite(self):
        return self._datacur - self._datastart

    cpdef void WriteByte(self, int number):
        self._data[self._datacur] = number & 0xFF
        self._datacur += 1

    cpdef void WriteWord(self, int number):
        self._data[self._datacur + 0] = number & 0xFF
        self._data[self._datacur + 1] = (number >> 8) & 0xFF
        self._datacur += 2

    cpdef void WriteDword(self, number2):
        cdef RlocInt_C number = constexpr.Evaluate(number2)

        if number.rlocmode:
            ut.ep_assert(
                self._datacur % 4 == 0,
                _('Non-const dwords must be aligned to 4byte')
            )
            if number.rlocmode == 1:
                self._prttable.append(self._datacur)
            elif number.rlocmode == 4:
                self._orttable.append(self._datacur)
            else:
                raise ut.EPError(_('rlocmode should be 1 or 4'))

        cdef unsigned int offset = number.offset & 0xFFFFFFFF
        self._data[self._datacur + 0] = offset & 0xFF
        self._data[self._datacur + 1] = (offset >> 8) & 0xFF
        self._data[self._datacur + 2] = (offset >> 16) & 0xFF
        self._data[self._datacur + 3] = (offset >> 24) & 0xFF
        self._datacur += 4

    def WritePack(self, structformat, arglist):
        '''
        ======= =======
          Char   Type
        ======= =======
           B     Byte
           H     Word
           I     Dword
        ======= =======
        '''

        cdef int* pdata
        try:
            pdata = <int*>PyCapsule_GetPointer(_packerData[structformat], "int*")
        except KeyError:
            pdata = CreateStructPackerData(structformat)
            _packerData[structformat] = PyCapsule_New(<void*>pdata, "int*", NULL)
        _StructPacker(pdata, self, arglist)

    def WriteBytes(self, b):
        '''
        Write bytes object to buffer.

        :param b: bytes object to write.
        '''
        if not isinstance(b, bytes):
            b = bytes(b)

        cdef char *raw = PyBytes_AsString(b)
        memcpy(&self._data[self._datacur], raw, len(b))
        self._datacur += len(b)

    cpdef void WriteSpace(self, size_t spacesize):
        self._datacur += spacesize

    # Internally used
    def CreatePayload(self):
        byteData = PyBytes_FromStringAndSize(<const char*>self._data, self._totlen)
        return Payload(byteData, self._prttable, self._orttable)


cdef int* CreateStructPackerData(str structformat):
    sizedict = {'B': 1, 'H': 2, 'I': 4}
    cdef int* sizelist = <int*>PyMem_Malloc(sizeof(int) * len(structformat))
    for i, s in enumerate(structformat):
        sizelist[i] = sizedict[s]

    return sizelist


cdef void _StructPacker(int* sizelist, PayloadBuffer buf, list arglist):
    cdef int dpos = buf._datacur
    cdef unsigned char* data = buf._data
    cdef list prttb = buf._prttable
    cdef list orttb = buf._orttable
    cdef RlocInt_C ri

    for i, arg in enumerate(arglist):
        argsize = sizelist[i]
        ri = constexpr.Evaluate(arg)

        if not (ri.rlocmode == 0 or (sizelist[i] == 4 and dpos % 4 == 0)):
            raise ut.EPError(
                _('Cannot write non-const in byte/word/nonalligned dword.')
            )

        if ri.rlocmode == 1:
            prttb.append(dpos)

        elif ri.rlocmode == 4:
            orttb.append(dpos)

        if sizelist[i] == 1:
            data[dpos] = ri.offset & 0xFF
            dpos += 1

        elif sizelist[i] == 2:
            (<uint32_t*>(data + dpos))[0] = ri.offset
            dpos += 2

        else:
            (<uint32_t*>(data + dpos))[0] = ri.offset
            dpos += 4

    buf._datacur = dpos

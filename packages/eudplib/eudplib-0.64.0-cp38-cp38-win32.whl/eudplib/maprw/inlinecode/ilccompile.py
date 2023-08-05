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


from ... import utils as ut
from ... import core as c
from ... import trigger as t
from ... import ctrlstru as cs
from ... import eudlib as sf

import types

_inlineGlobals = {}


def ComputeBaseInlineCodeGlobals():
    """
    Return list of globals inline eudplib code can call.
    """

    global _inlineGlobals

    # Add eudplib functions
    G = {}
    modules = [c, cs, sf, ut, t]
    for module in modules:
        for k, v in module.__dict__.items():
            if isinstance(v, types.ModuleType):
                continue
            if k[0] == "_":
                continue

            G[k] = v

    _inlineGlobals = G


def GetInlineCodeGlobals():
    """
    Return list of globals inline eudplib code can call.
    """

    G = _inlineGlobals.copy()

    # Add custom registered functions
    for k, v in c.GetEUDNamespace().items():
        G[k] = v

    return G


def CompileInlineCode(code):
    code = compile(code, "<string>", "exec")

    if c.PushTriggerScope():
        tStart = c.RawTrigger(actions=c.SetDeaths(0, c.SetTo, 0, 0))
        exec(code, GetInlineCodeGlobals(), {})
        tEnd = c.RawTrigger()
    c.PopTriggerScope()

    return (tStart, tEnd)

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

from eudplib import core as c, ctrlstru as cs


# Formula source : http://nghiaho.com/?p=997


@c.EUDFunc
def f_atan2(y, x):
    signflags = c.EUDVariable()
    signflags << 0

    # Check x sign
    if cs.EUDIf()(x >= 0x80000000):
        c.SeqCompute([(signflags, c.Add, 1), (x, c.SetTo, -x)])  # set xsign
    cs.EUDEndIf()

    # Check y sign
    if cs.EUDIf()(y >= 0x80000000):
        c.SeqCompute([(signflags, c.Add, 2), (y, c.SetTo, -y)])  # set ysign
    cs.EUDEndIf()

    # Check x/y order
    if cs.EUDIf()(y >= x):
        z = c.EUDVariable()
        # Swap x, y so that y <= x
        c.SeqCompute(
            [
                (signflags, c.Add, 4),  # set xyabscmp
                (z, c.SetTo, x),
                (x, c.SetTo, y),
                (y, c.SetTo, z),
            ]
        )
    cs.EUDEndIf()

    # To prevent overflow, we limit values of y and x.
    # atan value is maximized when x = y, then atan_value = 45 * x**3
    # 45 * x**3 <= 0xFFFFFFFF : x <= 456.99....
    if cs.EUDIf()(x >= 400):
        # Normalize below 400
        divn = x // 400
        divn += 1
        x //= divn
        y //= divn
    cs.EUDEndIf()

    # Calculate arctan value
    # arctan(z) ~= z * (45 - (z-1) * (14 + 4*z)), 0 <= z <= 1
    # arctan(y/x) ~= y/x * (45 - (y-x)/x * (14x + 4y)/x))
    # arctan(y/x) ~= y * (45*x*x - (y-x)(14x+4y)) / (x*x*x)
    t1 = x * x
    t2 = y * (45 * t1 - (y - x) * (14 * x + 4 * y))
    t3 = x * t1
    atan_value = t2 // t3

    # Translate angles by sign flags
    #
    #      |  0 |  1 | xsign          |  0 |  1 | xsign
    # -----+----+----+-----      -----+----+----+-----
    #   0  |  0+|180-|             0  | 90-| 90+|
    # -----+----+----+           -----+----+----+
    #   1  |360-|180+|             1  |270+|270-|
    # -----+----+----+           -----+----+----+
    # ysign|      xyabscmp=0     ysign|      xyabscmp=1

    cs.EUDSwitch(signflags)
    cs.EUDSwitchCase()(0)  # xsign, ysign, xyabscmp = 0, 0, 0
    c.EUDReturn(atan_value)
    cs.EUDSwitchCase()(1)  # xsign, ysign, xyabscmp = 1, 0, 0
    c.EUDReturn(180 - atan_value)
    cs.EUDSwitchCase()(2)  # xsign, ysign, xyabscmp = 0, 1, 0
    c.EUDReturn(360 - atan_value)
    cs.EUDSwitchCase()(3)  # xsign, ysign, xyabscmp = 1, 1, 0
    c.EUDReturn(180 + atan_value)
    cs.EUDSwitchCase()(4)  # xsign, ysign, xyabscmp = 0, 0, 1
    c.EUDReturn(90 - atan_value)
    cs.EUDSwitchCase()(5)  # xsign, ysign, xyabscmp = 1, 0, 1
    c.EUDReturn(90 + atan_value)
    cs.EUDSwitchCase()(6)  # xsign, ysign, xyabscmp = 0, 1, 1
    c.EUDReturn(270 + atan_value)
    cs.EUDSwitchCase()(7)  # xsign, ysign, xyabscmp = 1, 1, 1
    c.EUDReturn(270 - atan_value)
    cs.EUDEndSwitch()

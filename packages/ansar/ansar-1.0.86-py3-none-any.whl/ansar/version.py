# Author: Scott Woods <scott.suzuki@gmail.com>
# MIT License
#
# Copyright (c) 2017, 2018, 2019, 2020 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
"""
__docformat__ = 'restructuredtext'

__all__ = [
    'migrate',
]


def migrate(f, upgrade, *args, **kw_args):
    '''A function for auto-storing objects that change after an upgrade.

    :param upgrade: application upgrade code
    :type upgrade: function
    :param args: position upgrade args, optional
    :type args: list
    :param kw_args: key-word upgrade args, optional
    :type kw_args: dict
    :return: the recovered, upgraded and migrated object
    '''
    r, v = f.recover()
    a = upgrade(r, v, *args, **kw_args)
    if id(a) != id(r):
        f.store(a)
    return a

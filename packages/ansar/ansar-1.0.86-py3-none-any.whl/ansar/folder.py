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
The :py:class:`~ansar.folder.Folder` class provides for one-time description of folder location and
contents. The description is inherited by any child objects (i.e. ``Files``
and sub-``Folders``) created, and by operations within the folder.

The class also provides for persistence of maps. Rather than using a file
to store an entire map, the :py:class:`~ansar.folder.Folder` class can be used to store the
map on a one-file-per-entry basis.

.. autoclass:: Folder
   :members:
   :no-undoc-members:
"""

__docformat__ = 'restructuredtext'

__all__ = [
    'Folder',
]

import os
import errno
import re as regex

from .memory import *
from .runtime import *
from .message import *
from .codec import *
from .json import *
from .file import *

CREATE_FOLDER = 'create folder'
REMOVE_FOLDER = 'remove folder'
REMOVE_FILE = 'remove file'
#
#
def remove_folder(path):
    try:
        for f in os.listdir(path):
            p = os.path.join(path, f)
            if os.path.isdir(p):
                remove_folder(p)
            elif os.path.isfile(p):
                os.remove(p)
        os.rmdir(path)
    except OSError as e:
        if e.errno == errno.ENOENT:
            raise FileNotFound(REMOVE_FOLDER, p, 'name does not exist', e.errno)
        elif e.errno in (errno.EACCES, errno.EPERM):
            raise FileNoAccess(REMOVE_FOLDER, p, 'access or permissions', e.errno)
        elif e.errno == errno.ENOTDIR:
            raise FileNotAFile(REMOVE_FOLDER, p, 'name in path is not a folder', e.errno)
        raise FileFailure(REMOVE_FOLDER, p, 'unexpected platform code', code=0)

#
#
class Folder(object):
    '''Create and manage a collection of application values, using a folder.

    :param path: the location in the filesystem
    :type path: str
    :param te: formal description of the content
    :type te: :ref:`type expression<type-expressions>`
    :param re: formal description of expected file names
    :type re: a Python regular expression
    :param encoding: selection of representation, defaults to ``CodecJson``
    :type encoding: class
    :param pretty_format: generate human-readable file contents, defaults to ``True``
    :type pretty_format: bool
    :param decorate_names: auto-append an encoding-dependent extension to the file name, defaults to ``True``
    :type decorate_names: bool
    :param keys_names: a key-composer function and a name-composer function
    :type keys_names: 2-tuple of functions
    :param make_absolute: expand a relative path to be an absolute location, defaults to ``True``
    :type make_absolute: bool
    '''
    def __init__(self, path=None,
        te=None, re=None, encoding=None,
        pretty_format=True, decorate_names=True,
        create_default=False, keys_names=None,
        make_absolute=True):
        path = path or '.'
        if make_absolute:
            path = os.path.abspath(path)
        if te:
            te = fix_type(te)
        self.path = path
        if re is None:
            self.re = None
        else:
            self.re = regex.compile(re)
        self.te = te
        self.encoding = encoding or CodecJson
        self.pretty_format = pretty_format
        self.decorate_names = decorate_names
        self.create_default = create_default
        self.keys_names = keys_names


        try:
            os.makedirs(self.path)
        except OSError as e:
            if e.errno == errno.EEXIST:
                return
            elif e.errno in (errno.EACCES, errno.EPERM):
                raise FileNoAccess(CREATE_FOLDER, self.path, 'access or permissions', code=e.errno)
            elif e.errno == errno.ENOTDIR:
                raise FileNotAFile(CREATE_FOLDER, self.path, 'name in path is not a folder', code=e.errno)
            raise FileFailure(CREATE_FOLDER, self.path, 'unexpected platform code', code=e.errno)

    def folder(self, name, te=None, re=None, encoding=None,
        pretty_format=None, decorate_names=None, create_default=None, keys_names=None):
        '''Create a new :py:class:`~ansar.folder.Folder` object representing a sub-folder at the current location.

        :param path: the name to be added to the saved ``path``
        :type path: str
        :param te: formal description of the content
        :type te: :ref:`type expression<type-expressions>`
        :param re: formal description of expected file names
        :type re: a Python regular expression
        :param encoding: selection of representation, defaults to ``CodecJson``
        :type encoding: class
        :param pretty_format: generate human-readable file contents, defaults to ``True``
        :type pretty_format: bool
        :param decorate_names: auto-append an encoding-dependent extension to the file name, defaults to ``True``
        :type decorate_names: bool
        :param keys_names: a key-composer function and a name-composer function
        :type keys_names: 2-tuple of functions
        :param make_absolute: expand a relative path to be an absolute location, defaults to ``True``
        :type make_absolute: bool
        :return: a new location in the filesystem
        :rtype: :py:class:`~ansar.folder.Folder`
        '''
        if te:
            te = fix_type(te)
        te=te or self.te
        if re is None:
            self.re = None
        else:
            self.re = regex.compile(re)
        encoding=encoding or self.encoding
        if pretty_format is None: pretty_format = self.pretty_format
        if decorate_names is None: decorate_names = self.decorate_names
        if create_default is None: create_default = self.create_default
        keys_names=keys_names or self.keys_names

        path = os.path.join(self.path, name)
        return Folder(path, re=re, te=te, encoding=encoding,
            pretty_format=pretty_format, decorate_names=decorate_names, create_default=create_default,
            keys_names=keys_names, make_absolute=False)

    def file(self, name, te, encoding=None,
            pretty_format=None, decorate_names=None, create_default=None):
        '''Create a new :py:class:`~ansar.file.File` object representing a file at the current location.

        :param name: the name to be added to the saved ``path``
        :type name: str
        :param te: formal description of the content
        :type te: :ref:`type expression<type-expressions>`
        :param encoding: selection of representation, defaults to ``CodecJson``
        :type encoding: class
        :param pretty_format: generate human-readable file contents, defaults to ``True``
        :type pretty_format: bool
        :param decorate_names: auto-append an encoding-dependent extension to the file name, defaults to ``True``
        :type decorate_names: bool
        :param create_default: return default instance on file not found, defaults to ``False``
        :type create_default: bool
        :return: a new file in the filesystem
        :rtype: :py:class:`~ansar.file.File`
        '''
        # Fixed in File ctor.
        # te = fix_type(te)
        encoding=encoding or self.encoding
        if pretty_format is None: pretty_format = self.pretty_format
        if decorate_names is None: decorate_names = self.decorate_names
        if create_default is None: create_default = self.create_default

        path = os.path.join(self.path, name)    # Let the I/O operation decorate.
        return File(path, te, encoding=encoding,
            pretty_format=pretty_format, decorate_names=decorate_names, create_default=create_default)

    def matching(self):
        '''A generator method used to scan for files in the folder.

        :return: a sequence of filenames matching the :py:class:`~ansar.folder.Folder` criteria.
        :rtype: str
        '''
        re = self.re
        decorate_names = self.decorate_names
        extension = '.%s' % (self.encoding.EXTENSION,)
        for f in os.listdir(self.path):
            m = None
            p = os.path.join(self.path, f)
            if not os.path.isfile(p):
                continue
            if decorate_names:
                b, e = os.path.splitext(f)
                if e != extension:
                    continue
                f = b
            if re:
                m = re.match(f)
                if not m:
                    continue
            yield f

    def each(self):
        '''A generator method used to process the files in the folder.

        :return: a sequence of :py:class:`~ansar.file.File` objects matching the :py:class:`~ansar.folder.Folder` criteria.
        :rtype: :py:class:`~ansar.file.File`
        '''
        # Get a fresh image of folder/slice.
        # Use a snapshot for iteration to avoid
        # complications arising from changes to the folder.
        matched = [f for f in self.matching()]
        # Visit each named file.
        # Yield a file object, ready for I/O.
        for f in matched:
            yield self.file(f, self.te)

    def store(self, values):
        '''A method used to store a ``dict`` of values as files in the folder.

        :param values: a collection of application values
        :type values: dict
        :return: None.
        '''
        # Get a fresh image of folder/slice.
        matched = set(self.matching())
        stored = set()
        for k, v in values.items():
            name = self.name(v)
            io = self.file(name, self.te)
            io.store(v)
            stored.add(name)
        # Clean out files that look like they
        # have been previously written but are
        # no longer in the map.
        matched -= stored
        for m in matched:
            self.erase(m)

    def recover(self):
        '''A generator method used to recover application values from the files in the folder.

        :return: a sequence of 3-tuples, 0) key, 1) the value and 2) a version tag or ``None``
        :rtype: a 3-tuple
        '''
        # Get a fresh image of folder/slice.
        matched = [f for f in self.matching()]
        # Visit each named file.
        # Yield the key, message, version tuple.
        for f in matched:
            io = self.file(f, self.te)
            m, v = io.recover()
            k = self.key(m)
            yield k, m, v

    def add(self, values, item):
        '''A method used to add a value, both to a ``dict`` of values and as a file in the folder.

        :param values: a collection of application values
        :type values: dict
        :param item: the value to be added
        :type item: refer to ``Folder.te``
        '''
        keys_names = self.keys_names
        if keys_names is None:
            raise FileFailure('add to', self.path, 'key/name functions not set', code=0)

        key = keys_names[0](item)
        name = keys_names[1](item)

        io = self.file(name, self.te)
        if key in values:
            raise FileFailure('add', io.name, 'entry already present', code=0)
        io.store(item)
        values[key] = item

    def update(self, values, item):
        '''A method used to update a value, both in a ``dict`` of values and as a file in the folder.

        :param values: a collection of application values
        :type values: dict
        :param item: the value to be updated
        :type item: refer to ``Folder.te``
        '''
        keys_names = self.keys_names
        if keys_names is None:
            raise FileFailure('update', self.path, 'key/name functions not set', code=0)

        key = keys_names[0](item)
        name = keys_names[1](item)

        io = self.file(name, self.te)
        if key not in values:
            raise FileFailure('update', io.name, 'not an existing entry', code=0)

        io.store(item)
        values[key] = item

    def remove(self, values, item):
        '''A method used to remove a value, both from a ``dict`` of values and as a file in the folder.

        :param values: a collection of application values
        :type values: dict
        :param item: the value to be removed
        :type item: refer to ``Folder.te``
        '''
        keys_names = self.keys_names
        if keys_names is None:
            raise FileFailure('remove from', self.path, 'key/name functions not set', code=0)
        key = keys_names[0](item)
        name = keys_names[1](item)

        self.erase(name)
        del values[key]

    def clear(self, values):
        '''A method used to remove all values, both from a ``dict`` of values and as files in the folder.

        :param values: a collection of application values
        :type values: dict
        '''
        # Brute force. Delete any candidates from
        # the folder and dump everything from the dict.
        matched = [f for f in self.matching()]
        for removing in matched:
            self.erase(removing)
        values.clear()

    def erase(self, name):
        '''A method used to delete the named file from the folder.

        :param name: a name of a file
        :type name: str
        '''
        path = os.path.join(self.path, name)
        name = path
        if self.decorate_names:
            name = '%s.%s' % (path, self.encoding.EXTENSION)
        if os.path.isfile(name):
            try:
                os.remove(name)
            except IOError as e:
                if e.errno == errno.ENOENT:
                    raise FileNotFound(REMOVE_FILE, name, 'name does not exist', e.errno)
                elif e.errno in (errno.EACCES, errno.EPERM):
                    raise FileNoAccess(REMOVE_FILE, name, 'access or permissions', e.errno)
                elif e.errno == errno.ENOTDIR:
                    raise FileNotAFile(REMOVE_FILE, name, 'name in path is not a folder', e.errno)
                raise FileFailure(REMOVE_FILE, name, 'unexpected platform code', code=0)
            return True
        elif os.path.isdir(path):
            remove_folder(path)
            return True
        return False

    def exists(self, name):
        '''A method used to detect the named file, within the folder.

        :param name: a name of a file
        :type name: str
        :return: does the file exist
        :rtype: bool
        '''
        path = os.path.join(self.path, name)
        name = path
        if self.decorate_names:
            name = '%s.%s' % (path, self.encoding.EXTENSION)
        if os.path.isfile(name):
            return True
        elif os.path.isdir(path):
            return True
        return False

    def key(self, item):
        '''A method used to generate the stable key for a given application value.

        :param item: an application value
        :type name: see ``Folder.te``
        :return: the key
        :rtype: folder dependent
        '''
        keys_names = self.keys_names
        if keys_names is None:
            raise FileFailure('compose key', self.path, 'key/name functions not set', code=0)
        return keys_names[0](item)

    def name(self, item):
        '''A method used to generate the stable filename for a given application value.

        :param item: an application value
        :type name: see ``Folder.te``
        :return: the filename
        :rtype: str
        '''
        keys_names = self.keys_names
        if keys_names is None:
            raise FileFailure('compose name', self.path, 'key/name functions not set', code=0)
        return keys_names[1](item)

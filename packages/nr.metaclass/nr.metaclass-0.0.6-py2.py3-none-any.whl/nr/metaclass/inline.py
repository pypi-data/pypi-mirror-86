# -*- coding: utf8 -*-
# Copyright (c) 2019 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from .util import get_staticmethod_func, mro_resolve


class InlineMetaclass(type):
  """
  This is the metaclass for the #InlineMetaclassConstructor base class. It will
  call the special methods `__metanew__()` and `__metainit__()` of the
  constructed class. This avoids creating a new metaclass and allows to put the
  meta-constructor code in the same class.

  Note that the implementation does not take multiple inheritance into
  account and will simply call the first method found in the MRO.

  ```python
  class MyClass(metaclass=InlineMetaclass):
    def __metanew__(meta, name, bases, dict):
      # Do the stuff you would usually do in your metaclass.__new__()
      return super(InlineMetaclass, meta).__new__(meta, name, bases, dict)
    def __metainit__(cls, name, bases, dict):
      # Do the stuff you would usually do in your metaclass.__init__()
      pass
  ```
  """

  def __new__(cls, name, bases, dict):
    # Make sure the __metanew__() and __metainit__() functions
    # are classmethods.
    if '__metanew__' in dict:
      dict['__metanew__'] = staticmethod(dict['__metanew__'])
    if '__metainit__' in dict:
      dict['__metainit__'] = classmethod(dict['__metainit__'])

    # TODO: Py3k: Add the `__class__` cell to the metanew and metainit
    #       methods so that super() can be used.

    # Call the __metanew__() method if available.
    try:
      metanew = mro_resolve('__metanew__', bases, dict)
    except KeyError:
      return super(InlineMetaclass, cls).__new__(cls, name, bases, dict)
    else:
      if isinstance(metanew, staticmethod):
        metanew = get_staticmethod_func(metanew)
      return metanew(cls, name, bases, dict)

  def __init__(self, name, bases, dict):
    try:
      metainit = getattr(self, '__metainit__')
    except AttributeError:
      pass
    else:
      return metainit(name, bases, dict)


InlineMetaclassBase = InlineMetaclass('InlineMetaclassBase', (), {})

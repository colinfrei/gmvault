'''
    Gmvault: a tool to backup and restore your gmail account.
    Copyright (C) <2011-2012>  <guillaume Aubert (guillaume dot aubert at gmail do com)>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import collections

## {{{ http://code.activestate.com/recipes/576669/ (r18)
class OrderedDict(dict, collections.MutableMapping):

    # Methods with direct access to underlying attributes

    def __init__(self, *args, **kwds):
        if len(args) > 1:
            raise TypeError('expected at 1 argument, got %d', len(args))
        if not hasattr(self, '_keys'):
            self._keys = []
        self.update(*args, **kwds)

    def clear(self):
        del self._keys[:]
        dict.clear(self)

    def __setitem__(self, key, value):
        if key not in self:
            self._keys.append(key)
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._keys.remove(key)

    def __iter__(self):
        return iter(self._keys)

    def __reversed__(self):
        return reversed(self._keys)

    def popitem(self):
        if not self:
            raise KeyError
        key = self._keys.pop()
        value = dict.pop(self, key)
        return key, value

    def __reduce__(self):
        items = [[k, self[k]] for k in self]
        inst_dict = vars(self).copy()
        inst_dict.pop('_keys', None)
        return (self.__class__, (items,), inst_dict)

    # Methods with indirect access via the above methods

    setdefault = collections.MutableMapping.setdefault
    update     = collections.MutableMapping.update
    pop        = collections.MutableMapping.pop
    keys       = collections.MutableMapping.keys
    values     = collections.MutableMapping.values
    items      = collections.MutableMapping.items

    def __repr__(self):
        pairs = ', '.join(map('%r: %r'.__mod__, self.items()))
        return '%s({%s})' % (self.__class__.__name__, pairs)

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d
## end of http://code.activestate.com/recipes/576669/ }}}
class Map(object):
    """ Map wraps a dictionary. It is essentially an abstract class from which
    specific multimaps are subclassed. """
    def __init__(self):
        self._dict = {}
        
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self._dict))
    
    __str__ = __repr__
        
    def __getitem__(self, key):
        return self._dict[key]
    
    def __setitem__(self, key, value):
        self._dict[key] = value
    
    def __delitem__(self, key):
        del self._dict[key]
        
    def remove(self, key, value):
        del self._dict[key]
    
    def dict(self):
        """ Allows access to internal dictionary, if necessary. Caution: multimaps 
        will break if keys are not associated with proper container."""
        return self._dict

class ListMultimap(Map):
    """ ListMultimap is based on lists and allows multiple instances of same value. """
    def __init__(self):
        self._dict = collections.defaultdict(list)
        
    def __setitem__(self, key, value):
        self._dict[key].append(value)
    
    def remove(self, key, value):
        self._dict[key].remove(value)

class SetMultimap(Map):
    """ SetMultimap is based on sets and prevents multiple instances of same value. """
    def __init__(self):
        self._dict = collections.defaultdict(set)
        
    def __setitem__(self, key, value):
        self._dict[key].add(value)
    
    def remove(self, key, value):
        self._dict[key].remove(value)

class DictMultimap(Map):
    """ DictMultimap is based on dicts and allows fast tests for membership. """
    def __init__(self):
        self._dict = collections.defaultdict(dict)
        
    def __setitem__(self, key, value):
        self._dict[key][value] = True
    
    def remove(self, key, value):
        del self._dict[key][value]




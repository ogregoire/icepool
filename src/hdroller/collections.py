from functools import cached_property

class FrozenSortedWeights():
    """Immutable sorted dictionary whose values are integers.
    
    keys(), values(), and items() return tuples, which are subscriptable.
    """
    def __init__(self, d, remove_zero_weights=True):
        """
        Args:
            d: A dictionary of ints.
            remove_zero_weights: If True, zero weights will be omitted.
        """
        for key, value in d.items():
            if not isinstance(value, int):
                raise ValueError('Values must be ints, got ' + type(value).__name__)
            if value < 0:
                raise ValueError('Values must not be negative.')
        self._d = { k : d[k] for k in sorted(d.keys()) if not remove_zero_weights or d[k] > 0 }
    
    def __len__(self):
        return len(self._d)
    
    def __contains__(self, key):
        return key in self._d
    
    def __getitem__(self, key):
        return self._d.get(key, 0)
        
    @cached_property
    def _keys(self):
        return tuple(self._d.keys())
    
    def keys(self):
        return self._keys
    
    @cached_property
    def _values(self):
        return tuple(self._d.values())
    
    def values(self):
        return self._values
    
    @cached_property
    def _items(self):
        return tuple(self._d.items())
    
    def items(self):
        return self._items
    
    def __len__(self):
        return len(self._d)
    
    def pop_min(self):
        """Returns a copy of self with the min key removed, the popped key, and the popped value.
        
        Returns None, None, 0 if self has no elements remaining.
        """
        if len(self) > 0:
            return FrozenSortedWeights({ k : v for k, v in zip(self._keys[1:], self._values[1:]) }), self._keys[0], self._values[0]
        else:
            return None, None, 0
    
    def pop_max(self):
        """Returns a copy of self with the max key removed, the popped key, and the popped value.
        
        Returns None, None, 0 if self has no elements remaining.
        """
        if len(self) > 0:
            return FrozenSortedWeights({ k : v for k, v in zip(self._keys[:-1], self._values[:-1]) }), self._keys[-1], self._keys[-1]
        else:
            return None, None, 0

    def __str__(self):
        return str(self._d)
    
    def __repr__(self):
        return type(self).__name__ + f'({repr(self._d)})'
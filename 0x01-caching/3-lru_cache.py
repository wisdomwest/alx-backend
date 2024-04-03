#!/usr/bin/env python3
'''Create a class LRUCache that inherits from BaseCaching and is a caching
system:
You must use self.cache_data - dictionary from the parent class BaseCaching
You can overload def __init__(self): but don’t forget to call the parent
init: super().__init__()
def put(self, key, item):
Must assign to the dictionary self.cache_data the item value for the key key.
If key or item is None, this method should not do anything.
If the number of items in self.cache_data is higher that BaseCaching.MAX_ITEMS
you must discard the least recently used item (LRU algorithm)
you must print DISCARD: with the key discarded and following by a new line
def get(self, key):
Must return the value in self.cache_data linked to key.
If key is None or if the key doesn’t exist in self.cache_data, return None.'''

BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    '''LRU cache system'''

    def __init__(self):
        '''Init'''
        super().__init__()
        self.keys = []

    def put(self, key, item):
        '''Put in cache'''
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.keys.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            discard = self.keys.pop(0)
            del self.cache_data[discard]
            print('DISCARD:', discard)
        self.keys.append(key)
        self.cache_data[key] = item

    def get(self, key):
        '''Get from cache'''
        if key is None or key not in self.cache_data:
            return None
        self.keys.remove(key)
        self.keys.append(key)
        return self.cache_data[key]

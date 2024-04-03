#!/usr/bin/env python3
'''Create a class MRUCache that inherits from BaseCaching and is a caching
system
You must use self.cache_data - dictionary from the parent class BaseCaching
You can overload def __init__(self): but don’t forget to call the parent
init: super().__init__()
def put(self, key, item):
Must assign to the dictionary self.cache_data the item value for the key key.
If key or item is None, this method should not do anything.
If the number of items in self.cache_data is higher that BaseCaching.MAX_ITEMS
you must discard the most recently used item (MRU algorithm)
you must print DISCARD: with the key discarded and following by a new line
def get(self, key):
Must return the value in self.cache_data linked to key.
If key is None or if the key doesn’t exist in self.cache_data, return None.'''

BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    '''MRU cache system'''

    def __init__(self):
        '''Initilize MRU cache system'''
        super().__init__()
        self.keys = []

    def put(self, key, item):
        '''Add an item in the cache using MRU algorithm'''
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.keys.remove(key)

        if len(self.cache_data) >= self.MAX_ITEMS:
            mru_key = self.keys.pop()
            del self.cache_data[mru_key]
            print('DISCARD:', mru_key)

        self.keys.append(key)
        self.cache_data[key] = item

    def get(self, key):
        '''Get an item by key using MRU algorithm'''
        if key is None or key not in self.cache_data:
            return None

        self.keys.remove(key)
        self.keys.append(key)
        return self.cache_data[key]

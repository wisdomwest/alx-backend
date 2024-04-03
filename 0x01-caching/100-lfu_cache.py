#!/usr/bin/env python3
'''Create a class LFUCache that inherits from BaseCaching and is a caching
system:
You must use self.cache_data - dictionary from the parent class BaseCaching
You can overload def __init__(self): but don’t forget to call the parent
init: super().__init__()
def put(self, key, item):
Must assign to the dictionary self.cache_data the item value for the key key.
If key or item is None, this method should not do anything.
If the number of items in self.cache_data is higher that BaseCaching.MAX_ITEMS
you must discard the least frequency used item (LFU algorithm)
if you find more than 1 item to discard, you must use the LRU algorithm to
discard only the least recently used
you must print DISCARD: with the key discarded and following by a new line
def get(self, key):
Must return the value in self.cache_data linked to key.
If key is None or if the key doesn’t exist in self.cache_data, return None.'''

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    '''class LFUCache that inherits from BaseCaching and is a caching system'''

    def __init__(self):
        '''Init class'''
        super().__init__()
        self.lfu = {}

    def put(self, key, item):
        '''Must assign to the dictionary self.cache_data the item value for the
        key key'''
        if key is None or item is None:
            return
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            if key not in self.cache_data:
                lfu_keys = list(self.lfu.keys())
                lfu_keys.sort()
                lfu_key = lfu_keys[0]
                lru_keys = list(self.cache_data.keys())
                lru_key = lru_keys[0]
                if self.lfu[lfu_key] < self.cache_data[lru_key]:
                    del self.lfu[lfu_key]
                    del self.cache_data[lfu_key]
                    print('DISCARD:', lfu_key)
                else:
                    del self.cache_data[lru_key]
                    print('DISCARD:', lru_key)
        self.cache_data[key] = item
        if key in self.lfu:
            self.lfu[key] += 1
        else:
            self.lfu[key] = 1

    def get(self, key):
        '''Must return the value in self.cache_data linked to key'''
        if key is None or key not in self.cache_data:
            return None
        if key in self.lfu:
            self.lfu[key] += 1
        return self.cache_data[key]

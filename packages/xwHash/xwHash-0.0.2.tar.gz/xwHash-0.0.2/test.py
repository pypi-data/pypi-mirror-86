import xwHash

v = xwHash.fib(10)
print(v)

hash = xwHash.bkdrHash('abcd'.encode('utf8'));
print(hash)

hash = xwHash.cityHash('abcd'.encode('utf8'), 4)
print(hash)
hash = xwHash.cityHash('xbcd'.encode('utf8'), 4)
print(hash)

hash = xwHash.murmurHash3('xbcd'.encode('utf8'), 4)
print(hash)


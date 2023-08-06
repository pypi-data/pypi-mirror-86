from libc.stdint cimport uint32_t, uint64_t

cdef extern from "xhashes.h":
    unsigned int BKDRHash(char *str, unsigned int seed)
    double cfib(int n)

cdef extern from "City.h":
    uint64_t CityHash64(const char *buf, size_t len)

cdef extern from "MurmurHash3.h":
    void MurmurHash3_x86_32 (const void * key, int len, uint32_t seed, void * out)
    void MurmurHash3_x86_128(const void * key, int len, uint32_t seed, void * out)
    void MurmurHash3_x64_128(const void * key, int len, uint32_t seed, void * out)

#-------------------------------------------------------------------------------------
def fib(n):
    return cfib(n)

def bkdrHash(char* str):
    seed = 31              #31 131 1313 13131 131313 etc..
    hash = BKDRHash(str, seed)
    return hash

def cityHash(char *buf, int len):
    return CityHash64(buf, len)

def murmurHash3(char *str, int len):
    cdef uint64_t hashes[2]
    cdef int seed = 12345;

    MurmurHash3_x64_128(str, len, seed, hashes)
    return hashes[0]

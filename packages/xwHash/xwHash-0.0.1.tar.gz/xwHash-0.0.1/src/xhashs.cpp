// BKDR Hash Function
#include "xhashs.h"

unsigned int BKDRHash(char *str, unsigned int seed)
{
	unsigned int hash = 0;
 
	while (*str)
	{
		hash = hash * seed + (*str++);
	}
 
	return (hash & 0x7FFFFFFF);
}

double cfib(int n) 
{
    double a = 0.0, b = 1.0, tmp;
    int i;
    for (i=0; i<n; ++i) {
        tmp = a, a = a + b, b = tmp;
    }

    return a;
}

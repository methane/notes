#include <limits.h>
#include <stdbool.h>

bool add_overflow(unsigned long a, unsigned long b, unsigned long *out) {
    if (a > ULONG_MAX - b) {
        return true;
    }
    *out = a + b;
    return false;
}

bool add_overflow2(unsigned long a, unsigned long b, unsigned long *out) {
    return __builtin_add_overflow(a, b, out);
}


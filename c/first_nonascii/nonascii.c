#include <stddef.h>
#include <stdint.h>
#include <assert.h>
#include <memory.h>
#include <stdio.h>
#include <sys/types.h>


#define SIZEOF_SIZE_T 8
#define ALIGNOF_SIZE_T 8
#define ASCII_CHAR_MASK 0x8080808080808080ull
#define _Py_IS_ALIGNED(p, a) (!((uintptr_t)(p) & (uintptr_t)((a) - 1)))
#define _Py_ALIGN_UP(p, a) ((void *)(((uintptr_t)(p) + \
        (uintptr_t)((a) - 1)) & ~(uintptr_t)((a) - 1)))
#define _Py_ALIGN_DOWN(p, a) ((void *)((uintptr_t)(p) & ~(uintptr_t)((a) - 1)))


static inline unsigned int
ctz(size_t v)
{
    return __builtin_ctzll((unsigned long long)v);
}

ssize_t
first_nonascii0(const unsigned char *start, const unsigned char *end)
{
    const unsigned char *p = start;
    while (p < end) {
        if (*p & 0x80) {
            return p - start;
        }
        p++;
    }
    return p - start;
}

// load p[0]..p[size-1] as a little-endian size_t
// without unaligned access nor read ahead.
static inline size_t
load_unaligned_union(const unsigned char *p, size_t size)
{
    union {
        size_t u;
        unsigned char b[8];
    } t;
    t.u = 0;
    switch (size) {
    default:
    case 8:
        t.b[7] = p[7];
    // fall through
    case 7:
        t.b[6] = p[6];
    // fall through
    case 6:
        t.b[5] = p[5];
    // fall through
    case 5:
        t.b[4] = p[4];
    // fall through
    case 4:
        t.b[3] = p[3];
    // fall through
    case 3:
        t.b[2] = p[2];
    // fall through
    case 2:
        t.b[1] = p[1];
    // fall through
    case 1:
        t.b[0] = p[0];
        break;
    case 0:
        break;
    }
    return t.u;
}

static inline size_t
load_unaligned_shift(const unsigned char *p, size_t size)
{
    size_t u = 0;
    switch (size) {
    default:
    case 8:
        u |= (size_t)(p[7]) << 56;
    // fall through
    case 7:
        u |= (size_t)(p[6]) << 48;
    // fall through
    case 6:
        u |= (size_t)(p[5]) << 40;
    // fall through
    case 5:
        u |= (size_t)(p[4]) << 32;
    // fall through
    case 4:
        u |= (size_t)(p[3]) << 24;
    // fall through
    case 3:
        u |= (size_t)(p[2]) << 16;
    // fall through
    case 2:
        u |= (size_t)(p[1]) << 8;
    // fall through
    case 1:
        u |= (size_t)(p[0]);
        break;
    case 0:
        break;
    }
    return u;
}

static inline size_t
load_unaligned_memcpy(const unsigned char *p, size_t size)
{
    size_t u = 0;
    switch (size & 0x7) {
    default:
    case 8:
        memcpy(&u, p, 8);
        break;
    case 7:
        memcpy(&u, p, 7);
        break;
    case 6:
        memcpy(&u, p, 6);
        break;
    case 5:
        memcpy(&u, p, 5);
        break;
    case 4:
        memcpy(&u, p, 4);
        break;
    case 3:
        memcpy(&u, p, 3);
        break;
    case 2:
        memcpy(&u, p, 2);
        break;
    case 1:
        memcpy(&u, p, 1);
        break;
    case 0:
        break;
    }
    return u;
}


// use align up
ssize_t
first_nonascii1(const unsigned char *start, const unsigned char *end)
{
    const unsigned char *p = start;

    if (end - start >= SIZEOF_SIZE_T) {
        const unsigned char *p2 = _Py_ALIGN_UP(p, SIZEOF_SIZE_T);
        if (p < p2) {
            size_t u;
            memcpy(&u, p, sizeof(size_t));
            u &= ASCII_CHAR_MASK;
            if (u) {
                return (ctz(u) - 7) / 8;
            }
            p = p2;
        }

        const unsigned char *e = end - SIZEOF_SIZE_T;
        while (p <= e) {
            size_t u = (*(const size_t *)p) & ASCII_CHAR_MASK;
            if (u) {
                return p - start + (ctz(u) - 7) / 8;
            }
            p += SIZEOF_SIZE_T;
        }
    }

    while (p < end) {
        if (*p & 0x80) {
            return p - start;
        }
        p++;
    }
    return end - start;
}

// use align down
ssize_t
first_nonascii2(const unsigned char *start, const unsigned char *end)
{
    const unsigned char *p = start;

    if (end - start >= SIZEOF_SIZE_T) {
        size_t u;
        memcpy(&u, p, sizeof(size_t));
        u &= ASCII_CHAR_MASK;
        if (u) {
            return (ctz(u) - 7) / 8;
        }
        p = _Py_ALIGN_DOWN((p+SIZEOF_SIZE_T), SIZEOF_SIZE_T);

        const unsigned char *e = end - SIZEOF_SIZE_T;
        while (p <= e) {
            size_t u = (*(const size_t *)p) & ASCII_CHAR_MASK;
            if (u) {
                return p - start + (ctz(u) - 7) / 8;
            }
            p += SIZEOF_SIZE_T;
        }
    }

    while (p < end) {
        if (*p & 0x80) {
            return p - start;
        }
        p++;
    }
    return end - start;
}

// use load_unaligned_memcpy
ssize_t
first_nonascii3(const unsigned char *start, const unsigned char *end)
{
    const unsigned char *p = start;

    if (end - start >= SIZEOF_SIZE_T) {
        size_t u;
        memcpy(&u, p, sizeof(size_t));
        u &= ASCII_CHAR_MASK;
        if (u) {
            return (ctz(u) - 7) / 8;
        }
        p = _Py_ALIGN_DOWN((p+SIZEOF_SIZE_T), SIZEOF_SIZE_T);

        const unsigned char *e = end - SIZEOF_SIZE_T;
        while (p <= e) {
            size_t u = (*(const size_t *)p) & ASCII_CHAR_MASK;
            if (u) {
                return p - start + (ctz(u) - 7) / 8;
            }
            p += SIZEOF_SIZE_T;
        }
    }

#if 1
    size_t u = load_unaligned_memcpy(p, end-p);
#else
    size_t u=0;
    size_t s = end-p > 8 ? 8 : end-p;
    memcpy(&u, p, s);
#endif
    u &= ASCII_CHAR_MASK;
    if (u) {
        return p - start + (ctz(u) - 7) / 8;
    }

    return end - start;
}

// load_unaligned_shift
ssize_t
first_nonascii4(const unsigned char *start, const unsigned char *end)
{
    const unsigned char *p = start;

    if (end - start >= SIZEOF_SIZE_T) {
        size_t u;
        memcpy(&u, p, sizeof(size_t));
        u &= ASCII_CHAR_MASK;
        if (u) {
            return (ctz(u) - 7) / 8;
        }
        p = _Py_ALIGN_DOWN((p+SIZEOF_SIZE_T), SIZEOF_SIZE_T);

        const unsigned char *e = end - SIZEOF_SIZE_T;
        while (p <= e) {
            size_t u = (*(const size_t *)p) & ASCII_CHAR_MASK;
            if (u) {
                return p - start + (ctz(u) - 7) / 8;
            }
            p += SIZEOF_SIZE_T;
        }
    }

    size_t u = load_unaligned_shift(p, end-p);
    u &= ASCII_CHAR_MASK;
    if (u) {
        return p - start + (ctz(u) - 7) / 8;
    }
    return end - start;
}


// load_unaligned_union
ssize_t
first_nonascii5(const unsigned char *start, const unsigned char *end)
{
    const unsigned char *p = start;

    if (end - start >= SIZEOF_SIZE_T) {
        size_t u;
        memcpy(&u, p, sizeof(size_t));
        u &= ASCII_CHAR_MASK;
        if (u) {
            return (ctz(u) - 7) / 8;
        }
        p = _Py_ALIGN_DOWN((p+SIZEOF_SIZE_T), SIZEOF_SIZE_T);

        const unsigned char *e = end - SIZEOF_SIZE_T;
        while (p <= e) {
            size_t u = (*(const size_t *)p) & ASCII_CHAR_MASK;
            if (u) {
                return p - start + (ctz(u) - 7) / 8;
            }
            p += SIZEOF_SIZE_T;
        }
    }

    size_t u = load_unaligned_union(p, end-p);
    u &= ASCII_CHAR_MASK;
    if (u) {
        return p - start + (ctz(u) - 7) / 8;
    }
    return end - start;
}


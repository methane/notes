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
#if 1
static inline size_t
load_unaligned(const unsigned char *p, size_t size)
{
    assert(0 <= size && size <= 8);
    union {
        size_t u;
        unsigned char b[8];
    } t;
    t.u = 0;
    switch (size) {
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
        default:
            __builtin_unreachable();
    }
    return t.u;
}
#else
static inline size_t
load_unaligned(const unsigned char *p, size_t size)
{
    assert(0 <= size && size <= 7);
    size_t u = 0;
    switch (size & 0x7) {
//        case 8:
//            u |= (size_t)(p[7]) << 56;
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
        default:
            __builtin_unreachable();
    }
    return u;
}
#endif

// use size_t for aligned access
ssize_t
first_nonascii1(const unsigned char *start, const unsigned char *end)
{
    const unsigned char *p = start;

    if (end - start >= SIZEOF_SIZE_T) {
        while (!_Py_IS_ALIGNED(p, ALIGNOF_SIZE_T)) {
            if (*p & 0x80) {
                return p - start;
            }
            p++;
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

// use size_t for all access
ssize_t
first_nonascii2(const unsigned char *start, const unsigned char *end)
{
    const unsigned char *p = start;

    if (end - start >= SIZEOF_SIZE_T) {
        const unsigned char *p2 = _Py_ALIGN_UP(p, ALIGNOF_SIZE_T);
        // printf("unaligned access: %d\n", (int)(p2-p));
        if (p < p2) {
#if defined(_M_AMD64) || defined(_M_IX86) || defined(__x86_64__) || defined(__i386__)
            // does arm64 guarantee unaligned access?
            size_t u = *(const size_t*)p & ASCII_CHAR_MASK;
#else
            size_t u = load_unaligned(p, p2 - p) & ASCII_CHAR_MASK;
#endif
            if (u) {
                return p - start + (ctz(u) - 7) / 8;
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

    // assert((end-p) < sizeof(size_t));
    //if (p < end) {
        size_t u = load_unaligned(p, end - p) & ASCII_CHAR_MASK;
        if (u) {
            return p - start + (ctz(u) - 7) / 8;
        }
    //}
    return end - start;
}

// uses over the end read access.
ssize_t
first_nonascii3(const unsigned char *start, const unsigned char *end)
{
    const unsigned char *p = start;

    if (end - start >= SIZEOF_SIZE_T) {
        const unsigned char *e = _Py_ALIGN_UP(p, ALIGNOF_SIZE_T);
        // printf("unaligned access: %d\n", (int)(p2-p));
        if (p < e) {
#if defined(_M_AMD64) || defined(_M_IX86) || defined(__x86_64__) || defined(__i386__)
            // does arm64 guarantee unaligned access?
            size_t u = *(const size_t*)p & ASCII_CHAR_MASK;
#else
            size_t u = load_unaligned(p, p2 - p) & ASCII_CHAR_MASK;
#endif
            if (u) {
                return p - start + (ctz(u) - 7) / 8;
            }
            p = e;
        }
        e = end - SIZEOF_SIZE_T;
        while (p <= e) {
            size_t value = (*(const size_t *)p) & ASCII_CHAR_MASK;
            if (value) {
                return p - start + (ctz(value) - 7) / 8;
            }
            p += SIZEOF_SIZE_T;
        }
    }

    // cause read over the end.
    size_t u = *(size_t*)p & ((1ull << (end - p) * 8) - 1);
    if (u) {
        return p - start + (ctz(u) - 7) / 8;
    }
    return end - start;
}


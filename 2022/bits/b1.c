#include <stdio.h>
#include <stdint.h>

#if defined(__SSE2__) ||  \
    (defined(_MSC_VER) && \
     (defined(_M_X64) || (defined(_M_IX86) && _M_IX86_FP >= 2)))
#define HAVE_SSE2 1
#include <mmintrin.h>  //mmx
#include <emmintrin.h>
#else
#define HAVE_SSE2 0
#endif

/* CountTrailingZeroesNonzero64

This function is copied from:
https://github.com/abseil/abseil-cpp/blob/1ae9b71c474628d60eb251a3f62967fe64151bb2/absl/numeric/internal/bits.h#L273

License of this function:
// Copyright 2020 The Abseil Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

Modifications:

* Port to C, remove some macros.

*/
static inline int
CountTrailingZeroesNonzero64(uint64_t x) {
#if (defined(__clang__) || defined(__GNUC__))
    return __builtin_ctzll(x);
#elif defined(_MSC_VER) && !defined(__clang__) && \
    (defined(_M_X64) || defined(_M_ARM64))
    unsigned long result = 0;
    _BitScanForward64(&result, x);
    return result;
#elif defined(_MSC_VER) && !defined(__clang__)
    unsigned long result = 0;
    if ((uint32_t)(x) == 0) {
        _BitScanForward(&result, (uint32_t)(x >> 32));
        return result + 32;
    }
    _BitScanForward(&result, static_cast<unsigned long>(x));
    return result;
#else
    int c = 63;
    x &= ~x + 1;
    if (x & 0x00000000FFFFFFFF) c -= 32;
    if (x & 0x0000FFFF0000FFFF) c -= 16;
    if (x & 0x00FF00FF00FF00FF) c -= 8;
    if (x & 0x0F0F0F0F0F0F0F0F) c -= 4;
    if (x & 0x3333333333333333) c -= 2;
    if (x & 0x5555555555555555) c -= 1;
    return c;
#endif
}

// https://graphics.stanford.edu/~seander/bithacks.html#ZeroInWord

#define haszero(v) (((v) - 0x0101010101010101UL) & ~(v) & 0x8080808080808080UL)

#define hasvalue(x,n) \
    (haszero((x) ^ (~0UL/255 * (n))))

int main() {
    const unsigned long x = 0x0e120f1210121112;
    printf("x                   = %016lx\n", (x));
    //printf("~0UL/255            = %016lx\n", (~0UL/255)); // 0x101010...10
    printf("~0UL/255*0x12       = %016lx\n", (~0UL/255)*0x12);

    const unsigned long v = x^((~0UL/255)*0x12);
    printf("(x) ^ ~0UL/255*0x12 = %016lx = v\n", v);
    printf("v-0x010..01         = %016lx\n", v-0x0101010101010101UL);
    printf("~v                  = %016lx\n", ~v);
    printf("haszero(v)          = %016lx\n", haszero(v));

    uint64_t found = haszero(v);
    while (found) {
        int pos = CountTrailingZeroesNonzero64(found);
        pos >>= 3;
        printf("pos=%d\n", pos);
        found &= (found - 1);
    }


    printf("== MMX version ==\n");
    found = _mm_movemask_pi8(
                _mm_cmpeq_pi8(_mm_set1_pi8(0x12), _m_from_int64((int64_t)x)));
    printf("found = %x\n", found);
    while (found) {
        int pos = CountTrailingZeroesNonzero64(found);
        printf("pos=%d\n", pos);
        found &= (found - 1);
    }


    return 0;
}

#include <stdio.h>
#include <stdint.h>

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
    return 0;
}

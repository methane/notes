#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
#include <sys/types.h>
#include <string.h>
#include <time.h>
#include <memory.h>
#include <stdlib.h>

ssize_t
first_nonascii0(const unsigned char *start, const unsigned char *end);
ssize_t
first_nonascii1(const unsigned char *start, const unsigned char *end);
ssize_t
first_nonascii2(const unsigned char *start, const unsigned char *end);
ssize_t
first_nonascii3(const unsigned char *start, const unsigned char *end);
ssize_t
first_nonascii4(const unsigned char *start, const unsigned char *end);


void timespec_diff(struct timespec *start, struct timespec *stop,
                   struct timespec *result)
{
    if ((stop->tv_nsec - start->tv_nsec) < 0) {
        result->tv_sec = stop->tv_sec - start->tv_sec - 1;
        result->tv_nsec = stop->tv_nsec - start->tv_nsec + 1000000000;
    } else {
        result->tv_sec = stop->tv_sec - start->tv_sec;
        result->tv_nsec = stop->tv_nsec - start->tv_nsec;
    }
}



void longtest() {
    char *s = calloc(1000, 1);
    char *end = s + 1000;
    s[500] = 0x80;
    size_t a;
    for (int i = 0; i < 1000; i++) {
        printf("%d", i);
        a = first_nonascii0((const unsigned char*)s+i, (const unsigned char*)end);
        printf(" %ld", a);
        a = first_nonascii1((const unsigned char*)s+i, (const unsigned char*)end);
        printf(" %ld", a);
        a = first_nonascii2((const unsigned char*)s+i, (const unsigned char*)end);
        printf(" %ld", a);
        a = first_nonascii3((const unsigned char*)s+i, (const unsigned char*)end);
        printf(" %ld\n", a);
    }
}

int main()
{
    //longtest();

    const char *s = "abcdeabcdeabcdeabcde\xc0";
    const char *end = s + strlen(s);

    long long ll;
    long long cnt = 1000*1000;
    struct timespec start, stop, diff;

#if 1
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (ll = 0; ll < cnt; ll++) {
        first_nonascii0((const unsigned char*)s+(ll%8), (const unsigned char*)end);
    }
    clock_gettime(CLOCK_MONOTONIC, &stop);
    timespec_diff(&start, &stop, &diff);
    printf("0. %ld.%09ld ns\n", diff.tv_sec, diff.tv_nsec);
#endif

    clock_gettime(CLOCK_MONOTONIC, &start);
    for (ll = 0; ll < cnt; ll++) {
        first_nonascii1((const unsigned char*)s+(ll%8), (const unsigned char*)end);
    }
    clock_gettime(CLOCK_MONOTONIC, &stop);
    timespec_diff(&start, &stop, &diff);
    printf("1. %ld.%09ld ns\n", diff.tv_sec, diff.tv_nsec);

#if 1
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (ll = 0; ll < cnt; ll++) {
        first_nonascii2((const unsigned char*)s+(ll%8), (const unsigned char*)end);
    }
    clock_gettime(CLOCK_MONOTONIC, &stop);
    timespec_diff(&start, &stop, &diff);
    printf("2. %ld.%09ld ns\n", diff.tv_sec, diff.tv_nsec);
#endif

#if 1
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (ll = 0; ll < cnt; ll++) {
        first_nonascii3((const unsigned char*)s+(ll%8), (const unsigned char*)end);
    }
    clock_gettime(CLOCK_MONOTONIC, &stop);
    timespec_diff(&start, &stop, &diff);
    printf("3. %ld.%09ld ns\n", diff.tv_sec, diff.tv_nsec);
#endif

#if 1
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (ll = 0; ll < cnt; ll++) {
        first_nonascii4((const unsigned char*)s+(ll%8), (const unsigned char*)end);
    }
    clock_gettime(CLOCK_MONOTONIC, &stop);
    timespec_diff(&start, &stop, &diff);
    printf("4. %ld.%09ld ns\n", diff.tv_sec, diff.tv_nsec);
#endif

    return 0;
}


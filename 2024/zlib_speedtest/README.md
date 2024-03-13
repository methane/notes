### zlib compression ratio vs speed

I create this benchmark to determine which compression level to use in MySQL client/server protocol.

### how to run

Download `world.sql` from MySQL site.

https://dev.mysql.com/doc/index-other.html

### Compression ratio

```
$ go run main.go
query length=398629
level, compressed, ratio
    1,     104134, 0.261
    2,      99553, 0.250
    3,      98207, 0.246
    4,      95232, 0.239
    5,      92557, 0.232
    6,      92149, 0.231
    7,      91994, 0.231
    8,      90668, 0.227
    9,      90668, 0.227
```

* 1.1% difference between level 1 and 2.
* 1.1% difference between level 2 and 4.
* 1.2% difference between level 4 and 8.


### Compression speed

```
$ go test -bench .
goos: darwin
goarch: arm64
pkg: zlibspeed
Benchmark_Compress/level=1-8                 439           2482178 ns/op
Benchmark_Compress/level=2-8                 372           3312133 ns/op
Benchmark_Compress/level=3-8                 343           3567064 ns/op
Benchmark_Compress/level=4-8                 296           4042818 ns/op
Benchmark_Compress/level=5-8                 230           5089573 ns/op
Benchmark_Compress/level=6-8                 189           6227157 ns/op
Benchmark_Compress/level=7-8                 168           7120717 ns/op
Benchmark_Compress/level=8-8                 100          10219878 ns/op
Benchmark_Compress/level=9-8                 100          10422673 ns/op
PASS
ok      zlibspeed       14.205s
```

### Compression ratio by size

```
Comparing compression ratio by size, with level=2
uncmp len, cmp len, ratio
       50,      59, 1.180
      100,      84, 0.840
      150,      93, 0.620
      200,     111, 0.555
      250,     140, 0.560
      300,     161, 0.537
      350,     183, 0.523
      400,     200, 0.500
      450,     211, 0.469
```

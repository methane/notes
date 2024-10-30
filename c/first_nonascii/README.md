Intel(R) Core(TM) i5-12450H
Ubuntu 24.04

```
$ gcc -O3 -g nonascii.c main.c && ./a.out
0. 0.012176175 ns
1. 0.015173955 ns
2. 0.006761204 ns
3. 0.005399948 ns
```

M1 Pro MBP

```
$ clang -O3 -g nonascii.c main.c && ./a.out
0. 0.006126000 ns
1. 0.008504000 ns
2. 0.006774000 ns
3. 0.003173000 ns
```

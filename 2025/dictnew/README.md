Python 3.5

| Benchmark      | dict_new | dict_presized         |
|----------------|:--------:|:---------------------:|
| dict-1         | 454 ns   | 398 ns: 1.14x faster  |
| dict-5         | 2.07 us  | 1.73 us: 1.20x faster |
| dict-10        | 3.96 us  | 3.28 us: 1.21x faster |
| dict-25        | 9.25 us  | 7.56 us: 1.22x faster |
| dict-100       | 31.4 us  | 25.6 us: 1.22x faster |
| dict-500       | 113 us   | 103 us: 1.11x faster  |
| dict-1,000     | 218 us   | 200 us: 1.09x faster  |
| Geometric mean | (ref)    | 1.17x faster          |

Python 3.12

| Benchmark      | dict_new | dict_presized         |
|----------------|:--------:|:---------------------:|
| dict-1         | 378 ns   | 337 ns: 1.12x faster  |
| dict-5         | 1.49 us  | 1.34 us: 1.11x faster |
| dict-10        | 2.65 us  | 2.32 us: 1.14x faster |
| dict-25        | 5.84 us  | 5.12 us: 1.14x faster |
| dict-100       | 22.0 us  | 18.0 us: 1.22x faster |
| dict-500       | 98.6 us  | 87.6 us: 1.13x faster |
| dict-1,000     | 194 us   | 172 us: 1.13x faster  |
| Geometric mean | (ref)    | 1.14x faster          |


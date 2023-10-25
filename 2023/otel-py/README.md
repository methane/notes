# otel-py

measure overhead of instrumentations.

## text output

```py
# see script.py ...

#enable_ddtrace()
#enable_otel()

for _ in range(10000):
    test()
```

output:

```
# no instrument
$ time .venv/bin/python script.py

real	0m1.075s
user	0m1.024s
sys	0m0.032s

# opentelemetry
$ time .venv/bin/python script.py

real	0m11.381s
user	0m11.210s
sys	0m0.268s

# ddtrace
$ time .venv/bin/python script.py

real	0m7.821s
user	0m7.208s
sys	0m0.590s
```

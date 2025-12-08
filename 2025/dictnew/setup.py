from setuptools import setup, Extension

module1 = Extension('dictbench',
                    sources = ['dictbench.c'])

setup (name = 'DictBench',
       version = '1.0',
       description = 'Microbenchmark for dict creation',
       ext_modules = [module1])

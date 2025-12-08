#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <time.h>

static PyObject *bench_dict_new(PyObject *ob, PyObject *args) {
    Py_ssize_t size, loops;
    if (!PyArg_ParseTuple(args, "nn", &size, &loops)) {
        return NULL;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (Py_ssize_t loop = 0; loop < loops; loop++) {
        PyObject *d = PyDict_New();
        if (d == NULL) {
            return NULL;
        }

        for (Py_ssize_t i = 0; i < size; i++) {
            PyObject *key = PyUnicode_FromFormat("%zi", i);
            assert(key != NULL);

            PyObject *value = PyLong_FromLong(i);
            assert(value != NULL);

            PyDict_SetItem(d, key, value);
            Py_DECREF(key);
            Py_DECREF(value);
        }

        assert(PyDict_Size(d) == size);
        Py_DECREF(d);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_spent = (end.tv_sec - start.tv_sec) +
        (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    return PyFloat_FromDouble(time_spent);
}

static PyObject *bench_dict_presized(PyObject *ob, PyObject *args) {
    Py_ssize_t size, loops;
    if (!PyArg_ParseTuple(args, "nn", &size, &loops)) {
        return NULL;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (Py_ssize_t loop = 0; loop < loops; loop++) {
        PyObject *d = _PyDict_NewPresized(size);
        if (d == NULL) {
            return NULL;
        }

        for (Py_ssize_t i = 0; i < size; i++) {
            PyObject *key = PyUnicode_FromFormat("%zi", i);
            assert(key != NULL);

            PyObject *value = PyLong_FromLong(i);
            assert(value != NULL);

            PyDict_SetItem(d, key, value);
            Py_DECREF(key);
            Py_DECREF(value);
        }

        assert(PyDict_Size(d) == size);
        Py_DECREF(d);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_spent = (end.tv_sec - start.tv_sec) +
        (end.tv_nsec - start.tv_nsec) / 1000000000.0;
    return PyFloat_FromDouble(time_spent);
}

static PyMethodDef DictBenchMethods[] = {
    {"bench_new", bench_dict_new, METH_VARARGS, "Benchmark PyDict_New."},
    {"bench_presized", bench_dict_presized, METH_VARARGS,
        "Benchmark _PyDict_NewPresized."},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef dictbenchmodule = {
    PyModuleDef_HEAD_INIT, "dictbench", /* name of module */
    NULL,                               /* module documentation, may be NULL */
    -1, /* size of per-interpreter state of the module,
           or -1 if the module keeps state in global variables. */
    DictBenchMethods};

PyMODINIT_FUNC PyInit_dictbench(void) {
    return PyModule_Create(&dictbenchmodule);
}

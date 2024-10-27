#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *
decode1(PyObject *self, PyObject *arg)
{
    if (!PyBytes_Check(arg)) {
        PyErr_Format(PyExc_TypeError,
                "must be bytes, not %.100s",
                Py_TYPE(arg)->tp_name);
        return NULL;
    }
    char *buf;
    Py_ssize_t len;
    if (PyBytes_AsStringAndSize(arg, &buf, &len) < 0) {
        return NULL;
    }
    for (int i = 0; i < 999; i++) {
        PyObject *t = PyUnicode_FromStringAndSize(buf, len);
        Py_DECREF(t);
    }
    return PyUnicode_FromStringAndSize(buf, len);
}

// https://github.com/duckdb/duckdb/blob/56e2e0e5721b8547f564fccf252db0ba93c85471/tools/pythonpkg/src/numpy/array_wrapper.cpp#L215

int32_t UTF8ToCodepoint(const char *u_input, int &sz) {
	// from http://www.zedwood.com/article/cpp-utf8-char-to-codepoint
	auto u = reinterpret_cast<const unsigned char *>(u_input);
	unsigned char u0 = u[0];
	if (u0 <= 127) {
		sz = 1;
		return u0;
	}
	unsigned char u1 = u[1];
	if (u0 >= 192 && u0 <= 223) {
		sz = 2;
		return (u0 - 192) * 64 + (u1 - 128);
	}
	if (u[0] == 0xed && (u[1] & 0xa0) == 0xa0) {
		return -1; // code points, 0xd800 to 0xdfff
	}
	unsigned char u2 = u[2];
	if (u0 >= 224 && u0 <= 239) {
		sz = 3;
		return (u0 - 224) * 4096 + (u1 - 128) * 64 + (u2 - 128);
	}
	unsigned char u3 = u[3];
	if (u0 >= 240 && u0 <= 247) {
		sz = 4;
		return (u0 - 240) * 262144 + (u1 - 128) * 4096 + (u2 - 128) * 64 + (u3 - 128);
	}
	return -1;
}

#include <memory>
using namespace std;

typedef  Py_ssize_t idx_t;

struct StringConvert {
	template <class T>
	static void ConvertUnicodeValueTemplated(T *result, int32_t *codepoints, idx_t codepoint_count, const char *data,
	                                         idx_t ascii_count) {
		// we first fill in the batch of ascii characters directly
		for (idx_t i = 0; i < ascii_count; i++) {
			result[i] = data[i];
		}
		// then we fill in the remaining codepoints from our codepoint array
		for (idx_t i = 0; i < codepoint_count; i++) {
			result[ascii_count + i] = codepoints[i];
		}
	}

	static PyObject *ConvertUnicodeValue(const char *data, idx_t len, idx_t start_pos) {
		// slow path: check the code points
		// we know that all characters before "start_pos" were ascii characters, so we don't need to check those

		// allocate an array of code points so we only have to convert the codepoints once
		// short-string optimization
		// we know that the max amount of codepoints is the length of the string
		// for short strings (less than 64 bytes) we simply statically allocate an array of 256 bytes (64x int32)
		// this avoids memory allocation for small strings (common case)
		idx_t remaining = len - start_pos;
		unique_ptr<int32_t[]> allocated_codepoints;
		int32_t static_codepoints[64];
		int32_t *codepoints;
		if (remaining > 64) {
			allocated_codepoints = unique_ptr<int32_t[]>(new int32_t[remaining]);
			codepoints = allocated_codepoints.get();
		} else {
			codepoints = static_codepoints;
		}
		// now we iterate over the remainder of the string to convert the UTF8 string into a sequence of codepoints
		// and to find the maximum codepoint
		int32_t max_codepoint = 127;
		int sz;
		idx_t pos = start_pos;
		idx_t codepoint_count = 0;
		while (pos < len) {
			codepoints[codepoint_count] = UTF8ToCodepoint(data + pos, sz);
			pos += sz;
			if (codepoints[codepoint_count] > max_codepoint) {
				max_codepoint = codepoints[codepoint_count];
			}
			codepoint_count++;
		}
		// based on the max codepoint, we construct the result string
		auto result = PyUnicode_New(start_pos + codepoint_count, max_codepoint);
		// based on the resulting unicode kind, we fill in the code points
		// auto result_handle = py::handle(result);
		// auto kind = PyUtil::PyUnicodeKind(result_handle);
        int kind = PyUnicode_KIND(result);
		switch (kind) {
		case PyUnicode_1BYTE_KIND:
			ConvertUnicodeValueTemplated<Py_UCS1>(PyUnicode_1BYTE_DATA(result), codepoints,
			                                      codepoint_count, data, start_pos);
			break;
		case PyUnicode_2BYTE_KIND:
			ConvertUnicodeValueTemplated<Py_UCS2>(PyUnicode_2BYTE_DATA(result), codepoints,
			                                      codepoint_count, data, start_pos);
			break;
		case PyUnicode_4BYTE_KIND:
			ConvertUnicodeValueTemplated<Py_UCS4>(PyUnicode_4BYTE_DATA(result), codepoints,
			                                      codepoint_count, data, start_pos);
			break;
		default:
            PyErr_SetString(PyExc_SystemError, "bad typekind");
            return NULL;
			// throw NotImplementedException("Unsupported typekind constant '%d' for Python Unicode Compact decode", kind);
		}
		return result;
	}

	static PyObject *ConvertValue(const uint8_t *data, idx_t len) {
		// we could use PyUnicode_FromStringAndSize here, but it does a lot of verification that we don't need
		// because of that it is a lot slower than it needs to be
		// auto data = const_data_ptr_cast(val.GetData());
		// auto len = val.GetSize();
		// check if there are any non-ascii characters in there
		for (idx_t i = 0; i < len; i++) {
			if (data[i] > 127) {
				// there are! fallback to slower case
				return ConvertUnicodeValue((const char*)data, len, i);
			}
		}
		// no unicode: fast path
		// directly construct the string and memcpy it
		auto result = PyUnicode_New(len, 127);
		auto target_data = PyUnicode_1BYTE_DATA(result);
		memcpy(target_data, data, len);
		return result;
	}
};


static PyObject *
decode_duckdb(PyObject *self, PyObject *arg)
{
    if (!PyBytes_Check(arg)) {
        PyErr_Format(PyExc_TypeError,
                "must be bytes, not %.100s",
                Py_TYPE(arg)->tp_name);
        return NULL;
    }
    char *buf;
    Py_ssize_t len;
    if (PyBytes_AsStringAndSize(arg, &buf, &len) < 0) {
        return NULL;
    }
    for (int i = 0; i < 999; i++) {
        PyObject *t = StringConvert::ConvertValue((const uint8_t*)buf, len);
        Py_DECREF(t);
    }
    return StringConvert::ConvertValue((const uint8_t*)buf, len);
}

static PyMethodDef ext_methods[] = {
    {"decode1",  decode1, METH_O, "decode utf8 default"},
    {"decode_duckdb",  decode_duckdb, METH_O, "decode utf8 (duckdb)"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef extmodule = {
    PyModuleDef_HEAD_INIT,
    "ext",   /* name of module */
    "utf8 decoder functions", /* module documentation, may be NULL */
    0,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
    ext_methods,
};

PyMODINIT_FUNC
PyInit_ext(void)
{
    return PyModule_Create(&extmodule);
}

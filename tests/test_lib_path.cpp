#include <nanobind/nanobind.h>

#if defined(_MSC_VER)
#  define SHARED_LIB_IMPORT __declspec(dllimport)
#else
#  define SHARED_LIB_IMPORT
#endif

extern "C" SHARED_LIB_IMPORT int add(int a, int b);

NB_MODULE(test_lib_path_ext, m) {
    m.def("add", [](int a, int b) { return add(a, b); });
}

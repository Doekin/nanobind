#if defined(_MSC_VER)
#  define SHARED_LIB_EXPORT __declspec(dllexport)
#else
#  define SHARED_LIB_EXPORT
#endif

extern "C" SHARED_LIB_EXPORT int add(int a, int b) {
    return a + b;
}

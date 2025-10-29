import pytest
import os
import subprocess
import sys
import importlib.machinery

def test_stubgen_lib_path(tmp_path):
    # This test is not supported on PyPy
    if '__pypy__' in sys.builtin_module_names:
        pytest.skip("PyPy not supported in this test")

    # Define paths
    build_dir = os.path.join(tmp_path, "build")
    ext_module_path = os.path.join(build_dir, "test_lib_path_ext" + importlib.machinery.EXTENSION_SUFFIXES[0])

    # Determine shared library suffix based on platform
    if sys.platform == "win32":
        shared_lib_suffix = ".dll"
    elif sys.platform == "darwin":
        shared_lib_suffix = ".dylib"
    else:
        shared_lib_suffix = ".so"

    shared_lib_path = os.path.join(build_dir, "shared_lib" + shared_lib_suffix)
    stub_output_path = os.path.join(build_dir, "test_lib_path_ext.pyi")

    # Simulate the build process by creating dummy files
    os.makedirs(build_dir, exist_ok=True)
    with open(ext_module_path, "w") as f:
        f.write("dummy extension module")
    with open(shared_lib_path, "w") as f:
        f.write("dummy shared library")

    # Test 1: Stub generation should fail without LIB_PATH
    # We expect a ModuleNotFoundError or similar error because the shared library is not found
    cmd_fail = [
        sys.executable,
        "-m", "nanobind.stubgen",
        "-m", "test_lib_path_ext",
        "-i", build_dir,
        "-O", build_dir
    ]
    result_fail = subprocess.run(cmd_fail, capture_output=True, text=True)
    assert result_fail.returncode != 0, "Stub generation without LIB_PATH should fail"
    assert "ModuleNotFoundError" in result_fail.stderr or "ImportError" in result_fail.stderr, \
        "Expected ModuleNotFoundError or ImportError in stderr when LIB_PATH is missing"

    # Test 2: Stub generation should succeed with LIB_PATH
    cmd_success = [
        sys.executable,
        "-m", "nanobind.stubgen",
        "-m", "test_lib_path_ext",
        "-i", build_dir,
        "-O", build_dir,
        "-L", build_dir
    ]
    result_success = subprocess.run(cmd_success, capture_output=True, text=True)
    assert result_success.returncode == 0, \
        f"Stub generation with LIB_PATH should succeed, stderr: {result_success.stderr}"
    assert os.path.exists(stub_output_path), "Stub file should be generated"

    # Basic check for content (can be more robust if needed)
    with open(stub_output_path, "r") as f:
        content = f.read()
        assert "def add(arg0: int, arg1: int) -> int: ..." in content, \
            "Generated stub content is incorrect"

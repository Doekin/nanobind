import pytest
import os
import sys
from common import nanobind_example_ext_path, run_stubgen

def test01_stubgen_basic(tmp_path):
    """
    Tests that stubgen can be run on a simple module and that the generated
    stub file is valid Python.
    """

    ext_path = nanobind_example_ext_path()
    out_path = run_stubgen(ext_path, tmp_path)

    # The generated stub file should be valid Python.
    with open(out_path) as f:
        code = compile(f.read(), out_path, "exec")
    assert code is not None


def test02_stubgen_idempotent(tmp_path):
    """
    Tests that running stubgen on a module twice produces the same output.
    """

    ext_path = nanobind_example_ext_path()
    out_path_1 = run_stubgen(ext_path, tmp_path)
    out_path_2 = run_stubgen(ext_path, tmp_path)

    with open(out_path_1) as f:
        stub_1 = f.read()
    with open(out_path_2) as f:
        stub_2 = f.read()

    assert stub_1 == stub_2


def test03_no_sys_path_modification(tmp_path):
    """
    Tests that stubgen does not modify sys.path.
    """

    ext_path = nanobind_example_ext_path()

    original_sys_path = sys.path[:]
    run_stubgen(ext_path, tmp_path)
    assert sys.path == original_sys_path

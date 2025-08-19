# pi0quantum.py
# Self-contained Pi0System Python backbone with no external dependencies.

import ctypes
import os

# 4. Persistent registry of all operators
_OPERATORS = {}

def initialize_pi0system(lib_path=None):
    """
    Load the pi0core C library, bind all operators once,
    and populate the global _OPERATORS dict with Python wrappers.
    """
    # 1. Core Initialization
    if lib_path is None:
        lib_path = os.environ.get('PI0CORE_PATH', './pi0core.so')
    core = ctypes.CDLL(lib_path)

    # Bindings for C functions
    # pi0_diff1D: double* pi0_diff1D(const double*, size_t)
    core.pi0_diff1D.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_size_t)
    core.pi0_diff1D.restype  = ctypes.POINTER(ctypes.c_double)

    # pi0_laplace: double* pi0_laplace(const double*, size_t)
    core.pi0_laplace.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_size_t)
    core.pi0_laplace.restype  = ctypes.POINTER(ctypes.c_double)

    # pi0_spectral_project: void pi0_spectral_project(const double*, size_t, int, double*)
    core.pi0_spectral_project.argtypes = (
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_size_t,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_double)
    )
    core.pi0_spectral_project.restype = None

    # pi0_planck_diffusion: double* pi0_planck_diffusion(const double*, size_t, double)
    core.pi0_planck_diffusion.argtypes = (
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_size_t,
        ctypes.c_double
    )
    core.pi0_planck_diffusion.restype = ctypes.POINTER(ctypes.c_double)

    # 2. Internalizing wrappers into Python
    def diff1D(py_list):
        n = len(py_list)
        # prepare C array
        arr_type = ctypes.c_double * n
        c_arr = arr_type(*[float(v) for v in py_list])
        # call C
        out_ptr = core.pi0_diff1D(c_arr, n)
        # read back into Python list
        return [out_ptr[i] for i in range(n)]

    def laplace(py_list):
        n = len(py_list)
        arr_type = ctypes.c_double * n
        c_arr = arr_type(*[float(v) for v in py_list])
        out_ptr = core.pi0_laplace(c_arr, n)
        return [out_ptr[i] for i in range(n)]

    def spectral_project(py_list, scale_level):
        n = len(py_list)
        arr_type = ctypes.c_double * n
        c_in = arr_type(*[float(v) for v in py_list])
        c_out = arr_type()  # uninitialized output buffer
        core.pi0_spectral_project(c_in, n, int(scale_level), c_out)
        return [c_out[i] for i in range(n)]

    def planck_diffusion(py_list, lp2):
        n = len(py_list)
        arr_type = ctypes.c_double * n
        c_arr = arr_type(*[float(v) for v in py_list])
        out_ptr = core.pi0_planck_diffusion(c_arr, n, float(lp2))
        return [out_ptr[i] for i in range(n)]

    # 3. Populate the registry
    _OPERATORS['diff1D']             = diff1D
    _OPERATORS['laplace']            = laplace
    _OPERATORS['spectral_project']   = spectral_project
    _OPERATORS['planck_diffusion']   = planck_diffusion

    return _OPERATORS

# Expose for importers
__all__ = ['initialize_pi0system', '_OPERATORS']
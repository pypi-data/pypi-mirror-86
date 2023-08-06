"""Fast Fourier Transform Functions."""
import numpy as _numpy
import numpy.dual as _dual
import numpy.fft as _fft

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.libipp as _libipp
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.utils


class FFTFwd:
    """FFT forward Function."""

    __slots__ = (
        "_ipps_backend",
        "_numpy_callback",
        "_ipps_spec",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
    )
    _ipps_candidates = numpy_ipps.policies.float_candidates

    def __init__(self, order, dtype=_numpy.complex128):
        ipps_flag = numpy_ipps.utils.cast("int", 2)

        self._ipps_spec = numpy_ipps.utils.new("void**")

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_spec_buffer_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = _dispatch.ipps_function(
            "FFTGetSize-{}".format(
                "C" if dtype in numpy_ipps.policies.complex_candidates else "R"
            ),
            ("int", "int", "IppHintAlgorithm", " int*", " int*", " int*"),
            dtype,
        )
        ipps_fft_init = _dispatch.ipps_function(
            "FFTInit-{}".format(
                "C" if dtype in numpy_ipps.policies.complex_candidates else "R"
            ),
            ("void**", "int", "int", "IppHintAlgorithm", "void*", "void*"),
            dtype,
        )

        numpy_ipps.status = ipps_fft_getsize(
            order,
            ipps_flag,
            _libipp.ffi.typeof("IppHintAlgorithm").relements["ippAlgHintNone"],
            ipps_spec_size,
            ipps_spec_buffer_size,
            ipps_buffer_size,
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_size[0], dtype=_numpy.uint8)
        )
        ipps_mem_init = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_buffer_size[0], dtype=_numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )

        numpy_ipps.status = ipps_fft_init(
            self._ipps_spec,
            order,
            ipps_flag,
            _libipp.ffi.typeof("IppHintAlgorithm").relements["ippAlgHintNone"],
            self._ipps_mem_spec.cdata,
            ipps_mem_init.cdata,
        )

        self._ipps_backend = _dispatch.ipps_function(
            "FFTFwd-{}".format(
                "CToC"
                if dtype in numpy_ipps.policies.complex_candidates
                else "RToPerm"
            ),
            ("void*", "void*", "void*", "void*"),
            dtype,
        )

        self._numpy_callback = (
            _dual.fft
            if dtype in numpy_ipps.policies.complex_candidates
            else _fft.rfft
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = self._numpy_callback(src.ndarray)


class FFTInv:
    """FFT inverse Function."""

    __slots__ = (
        "_ipps_backend",
        "_numpy_callback",
        "_ipps_spec",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
    )
    _ipps_candidates = numpy_ipps.policies.float_candidates

    def __init__(self, order, dtype=_numpy.complex128):
        ipps_flag = numpy_ipps.utils.cast("int", 2)

        self._ipps_spec = numpy_ipps.utils.new("void**")

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_spec_buffer_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = _dispatch.ipps_function(
            "FFTGetSize-{}".format(
                "C" if dtype in numpy_ipps.policies.complex_candidates else "R"
            ),
            ("int", "int", "IppHintAlgorithm", " int*", " int*", " int*"),
            dtype,
        )
        ipps_fft_init = _dispatch.ipps_function(
            "FFTInit-{}".format(
                "C" if dtype in numpy_ipps.policies.complex_candidates else "R"
            ),
            ("void**", "int", "int", "IppHintAlgorithm", "void*", "void*"),
            dtype,
        )

        numpy_ipps.status = ipps_fft_getsize(
            order,
            ipps_flag,
            _libipp.ffi.typeof("IppHintAlgorithm").relements["ippAlgHintNone"],
            ipps_spec_size,
            ipps_spec_buffer_size,
            ipps_buffer_size,
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_size[0], dtype=_numpy.uint8)
        )
        ipps_mem_init = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_buffer_size[0], dtype=_numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )

        numpy_ipps.status = ipps_fft_init(
            self._ipps_spec,
            order,
            ipps_flag,
            _libipp.ffi.typeof("IppHintAlgorithm").relements["ippAlgHintNone"],
            self._ipps_mem_spec.cdata,
            ipps_mem_init.cdata,
        )

        self._ipps_backend = _dispatch.ipps_function(
            "FFTInv-{}".format(
                "CToC"
                if dtype in numpy_ipps.policies.complex_candidates
                else "PermToR"
            ),
            ("void*", "void*", "void*", "void*"),
            dtype,
        )

        self._numpy_callback = (
            _dual.ifft
            if dtype in numpy_ipps.policies.complex_candidates
            else _fft.irfft
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = self._numpy_callback(src.ndarray)


class ConjPerm(
    metaclass=_unaries.Unary,
    ipps_backend="ConjPerm",
    candidates=numpy_ipps.policies.complex_candidates,
):
    """ConjPerm Function."""

    pass


class ConjPerm_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="ConjPerm_I",
    candidates=numpy_ipps.policies.complex_candidates,
):
    """ConjPerm_I Function."""

    pass

"""Fast Fourier Transform Functions."""
import numpy as _numpy
import scipy.fftpack as _fft
import scipy.signal as _signal

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.libipp as _libipp
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.utils


class FFTFwd:
    """FFT forward Function.

    dst  <-  FFT[ src ]
    """

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
            _fft.fft
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
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = self._numpy_callback(src.ndarray)


class FFTInv:
    """FFT inverse Function.

    dst  <-  iFFT[ src ]
    """

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
            _fft.ifft
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
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

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


class _FIR_FFT_R:
    """FIR Function -- FFT Real implementation."""

    __slots__ = (
        "_ipps_backend_fft",
        "_ipps_backend_ifft",
        "_ipps_backend_mul",
        "_ipps_spec",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
        "_ipps_kernel",
        "_ipps_spectrum",
    )
    _ipps_candidates = numpy_ipps.policies.no_complex_candidates

    def __init__(self, kernel, order):
        ipps_flag = numpy_ipps.utils.cast("int", 2)

        self._ipps_spec = numpy_ipps.utils.new("void**")

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_spec_buffer_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = _dispatch.ipps_function(
            "FFTGetSize-R",
            ("int", "int", "IppHintAlgorithm", " int*", " int*", " int*"),
            kernel.dtype,
        )
        ipps_fft_init = _dispatch.ipps_function(
            "FFTInit-R",
            ("void**", "int", "int", "IppHintAlgorithm", "void*", "void*"),
            kernel.dtype,
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

        self._ipps_backend_fft = _dispatch.ipps_function(
            "FFTFwd-RToPerm",
            ("void*", "void*", "void*", "void*"),
            kernel.dtype,
        )
        self._ipps_backend_ifft = _dispatch.ipps_function(
            "FFTInv-PermToR",
            ("void*", "void*", "void*", "void*"),
            kernel.dtype,
        )

        self._ipps_backend_mul = numpy_ipps._detail.dispatch.ipps_function(
            "MulPerm_I",
            (
                "void*",
                "void*",
                "int",
            ),
            kernel.dtype,
        )

        kernel_pad = numpy_ipps.utils.ndarray(
            _numpy.zeros(1 << order, dtype=kernel.dtype)
        )
        kernel_pad.ndarray[: kernel.size] = kernel.flatten()
        self._ipps_kernel = numpy_ipps.utils.ndarray(
            _numpy.empty(1 << order, dtype=kernel.dtype)
        )
        numpy_ipps.status = self._ipps_backend_fft(
            kernel_pad.cdata,
            self._ipps_kernel.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )

        self._ipps_spectrum = numpy_ipps.utils.ndarray(
            _numpy.empty(1 << order, dtype=kernel.dtype)
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend_fft(
            src.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_mul(
            self._ipps_kernel.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spectrum.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_ifft(
            self._ipps_spectrum.cdata,
            dst.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class _FIR_FFT_C:
    """FIR Function -- FFT Complex implementation."""

    __slots__ = (
        "_ipps_backend_fft",
        "_ipps_backend_ifft",
        "_ipps_backend_mul",
        "_ipps_spec",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
        "_ipps_kernel",
        "_ipps_spectrum",
    )
    _ipps_candidates = numpy_ipps.policies.complex_candidates

    def __init__(self, kernel, order):
        ipps_flag = numpy_ipps.utils.cast("int", 2)

        self._ipps_spec = numpy_ipps.utils.new("void**")

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_spec_buffer_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fft_getsize = _dispatch.ipps_function(
            "FFTGetSize-C",
            ("int", "int", "IppHintAlgorithm", " int*", " int*", " int*"),
            kernel.dtype,
        )
        ipps_fft_init = _dispatch.ipps_function(
            "FFTInit-C",
            ("void**", "int", "int", "IppHintAlgorithm", "void*", "void*"),
            kernel.dtype,
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

        self._ipps_backend_fft = _dispatch.ipps_function(
            "FFTFwd-CToC",
            ("void*", "void*", "void*", "void*"),
            kernel.dtype,
        )
        self._ipps_backend_ifft = _dispatch.ipps_function(
            "FFTInv-CToC",
            ("void*", "void*", "void*", "void*"),
            kernel.dtype,
        )

        self._ipps_backend_mul = numpy_ipps._detail.dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                "Mul",
                kernel.dtype,
                numpy_ipps.policies.Accuracy.LEVEL_3,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            kernel.dtype,
        )

        kernel_pad = numpy_ipps.utils.ndarray(
            _numpy.zeros(1 << order, dtype=kernel.dtype)
        )
        kernel_pad.ndarray[: kernel.size] = kernel.flatten()
        self._ipps_kernel = numpy_ipps.utils.ndarray(
            _numpy.empty(1 << order, dtype=kernel.dtype)
        )
        numpy_ipps.status = self._ipps_backend_fft(
            kernel_pad.cdata,
            self._ipps_kernel.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )

        self._ipps_spectrum = numpy_ipps.utils.ndarray(
            _numpy.empty(1 << order, dtype=kernel.dtype)
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend_fft(
            src.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_mul(
            self._ipps_kernel.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spectrum.cdata,
            self._ipps_spectrum.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_ifft(
            self._ipps_spectrum.cdata,
            dst.cdata,
            self._ipps_spec[0],
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        raise NotImplementedError


class _FIR_Direct:
    """FIR Function -- Direct implementation."""

    __slots__ = (
        "_ipps_backend",
        "_ipps_mem_spec",
        "_ipps_mem_buffer",
        "_ipps_null",
        "_ipps_kernel",
        "_numpy_method",
    )
    _ipps_candidates = numpy_ipps.policies.float_candidates

    def __init__(self, kernel, method):
        if method == 0x00000001:
            self._numpy_method = "direct"
        elif method == 0x00000002:
            self._numpy_method = "fft"
        else:
            raise RuntimeError("Unknown method {}".format(method))

        self._ipps_kernel = numpy_ipps.utils.ndarray(kernel)

        ipps_flag = numpy_ipps.utils.cast("int", method)
        if self._ipps_kernel.ndarray.dtype == _numpy.float32:
            ipps_type = numpy_ipps.utils.cast("int", 13)
        elif self._ipps_kernel.ndarray.dtype == _numpy.float64:
            ipps_type = numpy_ipps.utils.cast("int", 19)
        elif self._ipps_kernel.ndarray.dtype == _numpy.complex64:
            ipps_type = numpy_ipps.utils.cast("int", 14)
        elif self._ipps_kernel.ndarray.dtype == _numpy.complex128:
            ipps_type = numpy_ipps.utils.cast("int", 20)
        else:
            raise RuntimeError(
                "Unknown dtype {}".format(self._ipps_kernel.ndarray.dtype)
            )
        self._ipps_null = numpy_ipps.utils.cast("void*", 0)

        ipps_spec_size = numpy_ipps.utils.new("int*")
        ipps_buffer_size = numpy_ipps.utils.new("int*")

        ipps_fir_getsize = _dispatch.ipps_function(
            "FIRSRGetSize",
            ("int", "int", "int*", " int*"),
        )
        ipps_fir_init = _dispatch.ipps_function(
            "FIRSRInit",
            ("void*", "int", "int", "void*"),
            self._ipps_kernel.ndarray.dtype,
        )

        numpy_ipps.status = ipps_fir_getsize(
            self._ipps_kernel.size,
            ipps_type,
            ipps_spec_size,
            ipps_buffer_size,
        )

        self._ipps_mem_spec = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_spec_size[0], dtype=_numpy.uint8)
        )
        self._ipps_mem_buffer = numpy_ipps.utils.ndarray(
            _numpy.empty(ipps_buffer_size[0], dtype=_numpy.uint8)
        )

        numpy_ipps.status = ipps_fir_init(
            self._ipps_kernel.cdata,
            self._ipps_kernel.size,
            ipps_flag,
            self._ipps_mem_spec.cdata,
        )

        self._ipps_backend = _dispatch.ipps_function(
            "FIRSR",
            ("void*", "void*", "int", "void*", "void*", "void*", "void*"),
            kernel.dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
            self._ipps_mem_spec.cdata,
            self._ipps_null,
            self._ipps_null,
            self._ipps_mem_buffer.cdata,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _signal.convolve(
            src.ndarray,
            self._ipps_kernel.ndarray,
            mode="same",
            method=self._numpy_method,
        )


def FIR(kernel):
    """Fir Function.

    dst  <-  convolve( src, kernel )
    """
    return _FIR_Direct(kernel, method=0x00000001)


FIR._ipps_candidates = _FIR_Direct._ipps_candidates
FIR.__call__ = _FIR_Direct.__call__

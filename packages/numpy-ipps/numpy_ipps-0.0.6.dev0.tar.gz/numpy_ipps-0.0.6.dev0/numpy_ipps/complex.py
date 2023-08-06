"""Complex Functions."""
import numpy as _numpy

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.utils


class Modulus(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Abs",
    numpy_backend=_numpy.absolute,
    candidates=numpy_ipps.policies.complex_candidates,
):
    """Abs Function."""

    pass


class Arg:
    """Arg Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                "Arg",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            ("void*", "void*", "signed int"),
            dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
        )

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _numpy.angle(src.ndarray)


class Real:
    """Real Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            "Real",
            ("void*", "void*", "int"),
            dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
        )

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _numpy.real(src.ndarray)


class Imag:
    """Imag Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            "Imag",
            ("void*", "void*", "int"),
            dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst.cdata,
            dst.size,
        )

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _numpy.imag(src.ndarray)


class RealToCplx:
    """RealToCplx Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            "RealToCplx",
            ("void*", "void*", "void*", "int"),
            dtype,
        )

    def __call__(self, src_re, src_im, dst):
        numpy_ipps.status = self._ipps_backend(
            src_re.cdata,
            src_im.cdata,
            dst.cdata,
            dst.size,
        )

    def _numpy_backend(self, src_re, src_im, dst):
        _numpy.multiply(1j, src_im.ndarray, dst.ndarray)
        _numpy.add(src_re.ndarray, dst.ndarray, dst.ndarray)


class _CplxToRealIPPSImpl:
    """CplxToReal Function -- Intel IPPS implementation."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            "CplxToReal",
            ("void*", "void*", "void*", "int"),
            dtype,
        )

    def __call__(self, src, dst_re, dst_im):
        numpy_ipps.status = self._ipps_backend(
            src.cdata,
            dst_re.cdata,
            dst_im.cdata,
            src.size,
        )

    def _numpy_backend(self, src, dst_re, dst_im):
        dst_re.ndarray[:] = _numpy.real(src.ndarray)
        dst_im.ndarray[:] = _numpy.imag(src.ndarray)


class _CplxToRealNumpyImpl:
    """CplxToReal Function -- Numpy implementation."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
            "CplxToReal",
            ("void*", "void*", "void*", "int"),
            dtype,
        )

    def __call__(self, src, dst_re, dst_im):
        dst_re.ndarray[:] = _numpy.real(src.ndarray)
        dst_im.ndarray[:] = _numpy.imag(src.ndarray)

    def _numpy_backend(self, src, dst_re, dst_im):
        dst_re.ndarray[:] = _numpy.real(src.ndarray)
        dst_im.ndarray[:] = _numpy.imag(src.ndarray)


def CplxToReal(size, dtype, accuracy=None):
    """CplxToReal Function."""
    return (
        _CplxToRealIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.complex128,)
        or accuracy is not None
        else _CplxToRealNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


CplxToReal._ipps_candidates = _CplxToRealIPPSImpl._ipps_candidates


class Conj(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Conj",
    numpy_backend=_numpy.conj,
    candidates=numpy_ipps.policies.complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Conj Function."""

    pass


class Conj_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Conj",
    numpy_backend=_numpy.conj,
    candidates=numpy_ipps.policies.complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Conj_I Function."""

    pass


class ConjFlip:
    """ConjFlip Function."""

    __slots__ = ("_ipps_backend_conj", "_ipps_backend_flip")
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = Conj._ipps_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend_conj = numpy_ipps._detail.dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                "Conj",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            ("void*", "void*", "signed int"),
            dtype,
        )
        self._ipps_backend_flip = _dispatch.ipps_function(
            "Flip_I",
            (
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend_conj(
            src.cdata,
            dst.cdata,
            dst.size,
        )
        numpy_ipps.status = self._ipps_backend_flip(
            dst.cdata,
            dst.size,
        )

    def _numpy_backend(self, src, dst):
        _numpy.conj(src.ndarray, dst.ndarray[::-1], casting="unsafe")


class ConjFlip_I:
    """ConjFlip_I Function."""

    __slots__ = ("_ipps_backend_conj", "_ipps_backend_flip")
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = Conj._ipps_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend_conj = numpy_ipps._detail.dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                "Conj",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            ("void*", "void*", "signed int"),
            dtype,
        )
        self._ipps_backend_flip = _dispatch.ipps_function(
            "Flip_I",
            (
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src_dst):
        numpy_ipps.status = self._ipps_backend_conj(
            src_dst.cdata,
            src_dst.cdata,
            src_dst.size,
        )
        numpy_ipps.status = self._ipps_backend_flip(
            src_dst.cdata,
            src_dst.size,
        )

    def _numpy_backend(self, src_dst):
        _numpy.conj(src_dst.ndarray, src_dst.ndarray[::-1], casting="unsafe")


class _MulByConjIPPSImpl:
    """MulByConj Function -- Intel IPPS implementation."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                "MulByConj",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )

    def __call__(self, src1, src2, dst):
        numpy_ipps.status = self._ipps_backend(
            src1.cdata,
            src2.cdata,
            dst.cdata,
            dst.size,
        )

    def _numpy_backend(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray, casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )


class _MulByConjNumpyImpl:
    """MulByConj Function -- Numpy implementation."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                "MulByConj",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )

    def __call__(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray, casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )

    def _numpy_backend(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray, casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )


def MulByConj(dtype, accuracy=None, size=None):
    """MulByConj Function."""
    return (
        _MulByConjIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if _numpy.dtype(dtype).itemsize not in (16,) or accuracy is not None
        else _MulByConjNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


MulByConj._ipps_candidates = _MulByConjIPPSImpl._ipps_candidates


class _MulByConjFlipIPPSImpl:
    """MulByConjFlip Function -- Intel IPPS implementation."""

    __slots__ = ("_ipps_backend_mulbyconj", "_ipps_backend_flip")
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend_mulbyconj = _dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                "MulByConj",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )
        self._ipps_backend_flip = _dispatch.ipps_function(
            "Flip",
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src1, src2, dst):
        numpy_ipps.status = self._ipps_backend_flip(
            src2.cdata,
            dst.cdata,
            dst.size,
        )
        numpy_ipps.status = self._ipps_backend_mulbyconj(
            src1.cdata,
            dst.cdata,
            dst.cdata,
            dst.size,
        )

    def _numpy_backend(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray[::-1], casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )


class _MulByConjFlipNumpyImpl:
    """MulByConjFlip Function -- Numpy implementation."""

    __slots__ = ("_ipps_backend_mulbyconj", "_ipps_backend_flip")
    _ipps_candidates = numpy_ipps.policies.complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend_mulbyconj = _dispatch.ipps_function(
            numpy_ipps._detail.dispatch.add_accurary(
                "MulByConj",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )
        self._ipps_backend_flip = _dispatch.ipps_function(
            "Flip",
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray[::-1], casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )

    def _numpy_backend(self, src1, src2, dst):
        _numpy.conj(src2.ndarray, dst.ndarray[::-1], casting="unsafe")
        _numpy.multiply(
            src1.ndarray, dst.ndarray, dst.ndarray, casting="unsafe"
        )


def MulByConjFlip(dtype, accuracy=None, size=None):
    """MulByConjFlip Function."""
    return (
        _MulByConjFlipIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if _numpy.dtype(dtype).itemsize not in (16,) or accuracy is not None
        else _MulByConjFlipNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


MulByConjFlip._ipps_candidates = _MulByConjFlipIPPSImpl._ipps_candidates

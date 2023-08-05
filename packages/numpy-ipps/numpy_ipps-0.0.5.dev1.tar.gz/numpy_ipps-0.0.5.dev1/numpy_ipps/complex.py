"""Complex Functions."""
import numpy as _numpy

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.utils


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


def MulByConj(size, dtype, accuracy=None):
    """MulByConj Function."""
    return (
        _MulByConjIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if 3 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (16,)
        or accuracy is not None
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


def MulByConjFlip(size, dtype, accuracy=None):
    """MulByConjFlip Function."""
    return (
        _MulByConjFlipIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or _numpy.dtype(dtype).itemsize not in (16,)
        or accuracy is not None
        else _MulByConjFlipNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


MulByConjFlip._ipps_candidates = _MulByConjFlipIPPSImpl._ipps_candidates

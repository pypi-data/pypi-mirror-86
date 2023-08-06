"""Exponential Functions."""
import numpy as _numpy
import scipy.special as _special

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.utils


class Exp(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Exp",
    numpy_backend=_numpy.exp,
):
    """Exp Function.

    dst[n]  <-  exp( src[n] )
    """

    pass


class Expm1(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Expm1",
    numpy_backend=_numpy.expm1,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Exp Function.

    dst[n]  <-  exp( src[n] ) - 1
    """

    pass


class _LnIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Ln",
    numpy_backend=_numpy.log,
):
    """Ln Function -- Intel IIPS implementatio."""

    pass


class _LnNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Ln",
    numpy_backend=_numpy.log,
    force_numpy=True,
):
    """Ln Function -- Numpy implementationv."""

    pass


def Ln(dtype, accuracy=None, size=None):
    """Ln Function.

    dst[n]  <-  ln( src[n] )
    """
    return (
        _LnIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _LnNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Ln._ipps_candidates = _LnIPPSImpl._ipps_candidates
Ln._ipps_accuracies = _LnIPPSImpl._ipps_accuracies
Ln.__call__ = _LnIPPSImpl.__call__


class Ln_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Ln",
    numpy_backend=_numpy.log,
    candidates=numpy_ipps.policies.complex_candidates,
):
    """Ln_I Function.

    src_dst[n]  <-  ln( src_dst[n] )
    """

    pass


class _Log10IPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Log10",
    numpy_backend=_numpy.log10,
):
    """Log10 Function -- Intel IPPS implementation."""

    pass


class _Log10NumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Log10",
    numpy_backend=_numpy.log10,
    force_numpy=True,
):
    """Log10 Function -- Numpy implementation."""

    pass


def Log10(dtype, accuracy=None, size=None):
    """Log10 Function.

    dst[n]  <-  log( src[n] )
    """
    return (
        _Log10IPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _Log10NumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Log10._ipps_candidates = _Log10IPPSImpl._ipps_candidates
Log10._ipps_accuracies = _Log10IPPSImpl._ipps_accuracies
Log10.__call__ = _Log10IPPSImpl.__call__


class Log1p(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Log1p",
    numpy_backend=_numpy.log1p,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Log1p Function.

    dst[n]  <-  ln( src[n] + 1 )
    """

    pass


class LogAddExp:
    """LogAddExp Function.

    dst[n]  <-  ln( exp( src1[n] ) + exp( src2[n] ) )
    """

    __slots__ = (
        "_ipps_backend_ln",
        "_ipps_backend_exp",
        "_ipps_backend_add",
        "_ipps_expLhs",
        "_ipps_expRhs",
        "_ipps_addLhsRhs",
    )
    _ipps_candidates = numpy_ipps.policies.float_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_expLhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_expRhs = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_backend_ln = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Ln",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )
        self._ipps_backend_exp = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Exp",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )
        self._ipps_backend_add = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Add",
                dtype,
                numpy_ipps.policies.Accuracy.LEVEL_3,
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
        numpy_ipps.status = self._ipps_backend_exp(
            src1.cdata,
            self._ipps_expLhs.cdata,
            src1.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_exp(
            src2.cdata,
            self._ipps_expRhs.cdata,
            src2.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_add(
            self._ipps_expLhs.cdata,
            self._ipps_expRhs.cdata,
            self._ipps_expRhs.cdata,
            dst.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_ln(
            self._ipps_expRhs.cdata,
            dst.cdata,
            dst.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src1, src2, dst):
        _numpy.logaddexp(
            src1.ndarray, src2.ndarray, dst.ndarray, casting="unsafe"
        )


class xLny:
    """xLny Function.

    dst[n]  <-  src1[n] * ln( src2[n] )
    """

    __slots__ = (
        "_ipps_backend_ln",
        "_ipps_backend_mul",
    )
    _ipps_candidates = numpy_ipps.policies.float_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend_ln = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Ln",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )
        self._ipps_backend_mul = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Mul",
                dtype,
                numpy_ipps.policies.Accuracy.LEVEL_3,
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
        numpy_ipps.status = self._ipps_backend_ln(
            src2.cdata,
            dst.cdata,
            dst.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_mul(
            src1.cdata,
            dst.cdata,
            dst.cdata,
            dst.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src1, src2, dst):
        dst.ndarray[:] = _special.xlogy(src1.ndarray, src2.ndarray)


class xLog1py:
    """xLog1py Function.

    dst[n]  <-  src1[n] * ln( src2[n] + 1 )
    """

    __slots__ = (
        "_ipps_backend_log1p",
        "_ipps_backend_mul",
    )
    _ipps_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend_log1p = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Log1p",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )
        self._ipps_backend_mul = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Mul",
                dtype,
                numpy_ipps.policies.Accuracy.LEVEL_3,
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
        numpy_ipps.status = self._ipps_backend_log1p(
            src2.cdata,
            dst.cdata,
            dst.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_mul(
            src1.cdata,
            dst.cdata,
            dst.cdata,
            dst.size,
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src1, src2, dst):
        dst.ndarray[:] = _special.xlog1py(src1.ndarray, src2.ndarray)

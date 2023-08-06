"""Special Functions."""
import numpy as _numpy
import scipy.special as _special

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies


class Erf:
    """Erf Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Erf",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, dst.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _special.erf(src.ndarray)


class Erfc(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Erfc",
    numpy_backend=_special.erfc,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Erfc Function."""

    pass


class Erfcx:
    """Erfcx Function."""

    __slots__ = (
        "_ipps_backend_erfc",
        "_ipps_backend_sqr",
        "_ipps_backend_exp",
        "_ipps_backend_mulI",
        "_ipps_sqr",
        "_ipps_exp",
    )
    _ipps_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_sqr = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )
        self._ipps_exp = numpy_ipps.utils.ndarray(
            _numpy.empty(size, dtype=dtype)
        )

        self._ipps_backend_erfc = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Erfc",
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
        self._ipps_backend_sqr = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Sqr",
                dtype,
                accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
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
        self._ipps_backend_mulI = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "Mul",
                dtype,
                accuracy=numpy_ipps.policies.Accuracy.LEVEL_3,
            ),
            (
                "void*",
                "void*",
                "void*",
                "signed int",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend_erfc(
            src.cdata, dst.cdata, dst.size
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_sqr(
            src.cdata, self._ipps_sqr.cdata, dst.size
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_exp(
            self._ipps_sqr.cdata, self._ipps_exp.cdata, dst.size
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)
        numpy_ipps.status = self._ipps_backend_mulI(
            self._ipps_exp.cdata, dst.cdata, dst.cdata, dst.size
        )
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        _special.erfcx(src.ndarray, dst.ndarray)


class ErfInv:
    """ErfInv Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "ErfInv",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, dst.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _special.erfinv(src.ndarray)


class ErfcInv:
    """ErfcInv Function."""

    __slots__ = ("_ipps_backend",)
    _ipps_candidates = numpy_ipps.policies.no_complex_candidates
    _ipps_accuracies = numpy_ipps.policies.default_accuracies

    def __init__(self, dtype, accuracy=None, size=None):
        self._ipps_backend = _dispatch.ipps_function(
            _dispatch.add_accurary(
                "ErfcInv",
                dtype,
                accuracy=self._ipps_accuracies[-1]
                if accuracy is None
                else accuracy,
            ),
            (
                "void*",
                "void*",
                "int",
            ),
            dtype,
        )

    def __call__(self, src, dst):
        numpy_ipps.status = self._ipps_backend(src.cdata, dst.cdata, dst.size)
        assert (
            numpy_ipps.status == 0
        ), "DEBUG: Bad Intel IPP Signal status {}".format(numpy_ipps.status)

    def _numpy_backend(self, src, dst):
        dst.ndarray[:] = _special.erfcinv(src.ndarray)


class CdfNorm(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="CdfNorm",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """CdfNorm Function."""

    pass


class CdfNormInv(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="CdfNormInv",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """CdfNormInv Function."""

    pass

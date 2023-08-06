"""Complex Functions."""
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies


class Erf(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Erf",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Erf Function."""

    pass


class Erfc(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Erfc",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Erfc Function."""

    pass


class ErfInv(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="ErfInv",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """ErfInv Function."""

    pass


class ErfInv_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="ErfInv",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """ErfInv_I Function."""

    pass


class ErfcInv(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="ErfcInv",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """ErfcInv Function."""

    pass


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


class CdfNormInv_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="CdfNormInv",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """CdfNormInv_I Function."""

    pass

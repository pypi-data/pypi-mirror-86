"""Trigonometric and Hyperbolic Functions."""
import numpy as _numpy

import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies


class _CosIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Cos",
    numpy_backend=_numpy.cos,
):
    """Cos Function -- Intel IPPS implementation."""

    pass


class _CosNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Cos",
    numpy_backend=_numpy.cos,
    force_numpy=True,
):
    """Cos Function -- Numpy implementation."""

    pass


def Cos(dtype, accuracy=None, size=None):
    """Cos Function."""
    return (
        _CosIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _CosNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Cos._ipps_candidates = _CosIPPSImpl._ipps_candidates


class Cos_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Cos",
    numpy_backend=_numpy.cos,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Cos_I Function."""

    pass


class _SinIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sin",
    numpy_backend=_numpy.sin,
):
    """Sin Function -- Intel IPPS implementation."""

    pass


class _SinNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sin",
    numpy_backend=_numpy.sin,
    force_numpy=True,
):
    """Sin Function -- Numpy implementation."""

    pass


def Sin(dtype, accuracy=None, size=None):
    """Cos Function."""
    return (
        _SinIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _SinNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Sin._ipps_candidates = _SinIPPSImpl._ipps_candidates


class Sin_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Sin",
    numpy_backend=_numpy.sin,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Sin_I Function."""

    pass


class _TanIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Tan",
    numpy_backend=_numpy.tan,
):
    """Tan Function -- Intel IPPS implementation."""

    pass


class _TanNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Tan",
    numpy_backend=_numpy.tan,
    force_numpy=True,
):
    """Tan Function -- Numpy implementation."""

    pass


def Tan(dtype, accuracy=None, size=None):
    """Cos Function."""
    return (
        _TanIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _TanNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Tan._ipps_candidates = _TanIPPSImpl._ipps_candidates


class Tan_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Tan",
    numpy_backend=_numpy.tan,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Tan_I Function."""

    pass


class _AcosIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Acos",
    numpy_backend=_numpy.arccos,
):
    """Acos Function -- Intel IPPS implementation."""

    pass


class _AcosNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Acos",
    numpy_backend=_numpy.arccos,
    force_numpy=True,
):
    """Acos Function -- Numpy implementation."""

    pass


def Acos(dtype, accuracy=None, size=None):
    """Acos Function."""
    return (
        _TanIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _AcosNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Acos._ipps_candidates = _AcosIPPSImpl._ipps_candidates


class _AsinIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Asin",
    numpy_backend=_numpy.arcsin,
):
    """Asin Function -- Intel IPPS implementation."""

    pass


class _AsinNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Asin",
    numpy_backend=_numpy.arcsin,
    force_numpy=True,
):
    """Asin Function -- Numpy implementation."""

    pass


def Asin(dtype, accuracy=None, size=None):
    """Asin Function."""
    return (
        _AsinIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _AsinNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Asin._ipps_candidates = _AsinIPPSImpl._ipps_candidates


class Asin_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Asin",
    numpy_backend=_numpy.arcsin,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Asin_I Function."""

    pass


class _AtanIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Atan",
    numpy_backend=_numpy.arctan,
):
    """Atan Function."""

    pass


class _AtanNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Atan",
    numpy_backend=_numpy.arctan,
    force_numpy=True,
):
    """Atan Function."""

    pass


def Atan(dtype, accuracy=None, size=None):
    """Atan Function."""
    return (
        _AtanIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _AtanNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Atan._ipps_candidates = _AtanIPPSImpl._ipps_candidates


class Atan_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Atan",
    numpy_backend=_numpy.arctan,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Atan_I Function."""

    pass


class Cosh(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Cosh",
    numpy_backend=_numpy.cosh,
):
    """Cosh Function."""

    pass


class Sinh(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sinh",
    numpy_backend=_numpy.sinh,
):
    """Sinh Function."""

    pass


class _SinhIIPPSImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Sinh",
    numpy_backend=_numpy.sinh,
    candidates=numpy_ipps.policies.complex_candidates,
):
    """Sinh_I Function -- Intel IPPS implementation."""

    pass


class _SinhINumpyImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Sinh",
    numpy_backend=_numpy.sinh,
    candidates=numpy_ipps.policies.complex_candidates,
    force_numpy=True,
):
    """Sinh_I Function -- Numpy implementation."""

    pass


def Sinh_I(size, dtype, accuracy=None):
    """Sinh_I Function."""
    return (
        _SinhIIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.complex128,)
        or accuracy is not None
        else _SinhINumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Sinh_I._ipps_candidates = _SinhIIPPSImpl._ipps_candidates


class _TanhIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Tanh",
    numpy_backend=_numpy.tanh,
):
    """Tanh Function -- Intel IPPS implementation."""

    pass


class _TanhNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Tanh",
    numpy_backend=_numpy.tanh,
    force_numpy=True,
):
    """Tanh Function -- Numpy implementation."""

    pass


def Tanh(size, dtype, accuracy=None):
    """Tanh Function."""
    return (
        _TanhIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _TanhNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Tanh._ipps_candidates = _TanhIPPSImpl._ipps_candidates


class _TanhIIPPSImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Tanh",
    numpy_backend=_numpy.tanh,
):
    """Tanh_I Function -- Intel IPPS implementation."""

    pass


class _TanhINumpyImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Tanh",
    numpy_backend=_numpy.tanh,
    force_numpy=True,
):
    """Tanh_I Function -- Numpy implementation."""

    pass


def Tanh_I(size, dtype, accuracy=None):
    """Tanh_I Function."""
    return (
        _TanhIIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _TanhINumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Tanh_I._ipps_candidates = _TanhIIPPSImpl._ipps_candidates


class _AcoshIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Acosh",
    numpy_backend=_numpy.arccosh,
):
    """Acosh Function -- Intel IPPS implementation."""

    pass


class _AcoshNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Acosh",
    numpy_backend=_numpy.arccosh,
    force_numpy=True,
):
    """Acosh Function -- Numpy implementation."""

    pass


def Acosh(dtype, accuracy=None, size=None):
    """Acosh Function."""
    return (
        _AcoshIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _AcoshNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Acosh._ipps_candidates = _AcoshIPPSImpl._ipps_candidates


class _AsinhIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Asinh",
    numpy_backend=_numpy.arcsinh,
):
    """Asinh Function -- Intel IPPS implementation."""

    pass


class _AsinhNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Asinh",
    numpy_backend=_numpy.arcsinh,
    force_numpy=True,
):
    """Asinh Function -- Numpy implementation."""

    pass


def Asinh(dtype, accuracy=None, size=None):
    """Asinh Function."""
    return (
        _AsinhIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _AsinhNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Asinh._ipps_candidates = _AsinhIPPSImpl._ipps_candidates


class _AsinhIIPPSImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Asinh",
    numpy_backend=_numpy.arcsinh,
):
    """Asinh_I Function -- Intel IPPS implementation."""

    pass


class _AsinhINumpyImpl(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Asinh",
    numpy_backend=_numpy.arcsinh,
    force_numpy=True,
):
    """Asinh_I Function -- Numpy implementation."""

    pass


def Asinh_I(size, dtype, accuracy=None):
    """Asinh_I Function."""
    return (
        _AsinhIIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.complex128,)
        or accuracy is not None
        else _AsinhINumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Asinh_I._ipps_candidates = _AsinhIIPPSImpl._ipps_candidates


class _AtanhIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Atanh",
    numpy_backend=_numpy.arctanh,
):
    """Atanh Function -- Intel IPPS implementation."""

    pass


class _AtanhNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Atanh",
    numpy_backend=_numpy.arctanh,
    force_numpy=True,
):
    """Atanh Function -- Numpy implementation."""

    pass


def Atanh(size, dtype, accuracy=None):
    """Atanh Function."""
    return (
        _AtanhIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _AtanhNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Atanh._ipps_candidates = _AtanhIPPSImpl._ipps_candidates


class Atan2(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Atan2",
    numpy_backend=_numpy.arctan2,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Atan2 Function."""

    pass


class Atan2Rev_I(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Atan2",
    numpy_backend=_numpy.arctan2,
    candidates=numpy_ipps.policies.no_complex_candidates,
    numpy_swap=True,
    reverse=True,
):
    """Atan2Rev_I Function."""

    pass


class Hypot(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Hypot",
    numpy_backend=_numpy.hypot,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Hypot Function."""

    pass

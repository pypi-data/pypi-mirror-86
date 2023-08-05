"""Complex Functions."""
import numpy as _numpy

import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.unaries as _unaries
import numpy_ipps.policies
import numpy_ipps.support
import numpy_ipps.utils


class Sqr(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sqr",
    numpy_backend=_numpy.square,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Sqr Function."""

    pass


class Sqr_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Sqr",
    numpy_backend=_numpy.square,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Sqr_I Function."""

    pass


class Abs(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Abs",
    numpy_backend=_numpy.fabs,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Abs Function."""

    pass


class Abs_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Abs",
    numpy_backend=_numpy.fabs,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Abs_I Function."""

    pass


class _SqrtIPPSImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sqrt",
    numpy_backend=_numpy.sqrt,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Sqrt Function -- Intel IPPS implementation."""

    pass


class _SqrtNumpyImpl(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Sqrt",
    numpy_backend=_numpy.sqrt,
    force_numpy=True,
):
    """Sqrt Function -- Numpy implementation."""

    pass


def Sqrt(size, dtype, accuracy=None):
    """Sqrt Function."""
    if accuracy is not None:
        if dtype == _numpy.complex128:
            return _SqrtNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
        elif 2 * size * _numpy.dtype(
            dtype
        ).itemsize < numpy_ipps.support.L1 or _numpy.dtype(
            dtype
        ).itemsize not in (
            8,
        ):
            return _SqrtIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        return _SqrtNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    else:
        return _SqrtIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)


Sqrt._ipps_candidates = _SqrtIPPSImpl._ipps_candidates


class Sqrt_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Sqrt",
    numpy_backend=_numpy.sqrt,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Sqrt_I Function."""

    pass


class Cbrt(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Cbrt",
    numpy_backend=_numpy.cbrt,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Cbrt Function."""

    pass


class Cbrt_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Cbrt",
    numpy_backend=_numpy.cbrt,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Cbrt_I Function."""

    pass


class Inv(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Inv",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Inv Function."""

    pass


class Inv_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Inv",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Inv_I Function."""

    pass


class InvSqrt(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="InvSqrt",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """InvSqrt Function."""

    pass


class InvSqrt_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="InvSqrt",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """InvSqrt_I Function."""

    pass


class InvCbrt(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="InvCbrt",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """InvCbrt Function."""

    pass


class InvCbrt_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="InvCbrt",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """InvCbrt_I Function."""

    pass


class Pow2o3(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Pow2o3",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Pow2o3 Function."""

    pass


class Pow2o3_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Pow2o3",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Pow2o3_I Function."""

    pass


class Pow3o2(
    metaclass=_unaries.UnaryAccuracy,
    ipps_backend="Pow3o2",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Pow3o2 Function."""

    pass


class Pow3o2_I(
    metaclass=_unaries.UnaryAccuracy_I,
    ipps_backend="Pow3o2",
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Pow3o2_I Function."""

    pass


class _AddIPPSImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Add",
    numpy_backend=_numpy.add,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Add Function -- Intel IPPS implementation."""

    pass


class _AddNumpyImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Add",
    numpy_backend=_numpy.add,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    force_numpy=True,
):
    """Add Function -- Numpy implementation."""

    pass


def Add(size, dtype, accuracy=None):
    """Add Function."""
    return (
        _AddIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if 3 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _AddNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Add._ipps_candidates = _AddIPPSImpl._ipps_candidates


class Add_I(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Add",
    numpy_backend=_numpy.add,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Add_I Function."""

    pass


class _SubIPPSImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Sub Function -- Intel IPPS implementation."""

    pass


class _SubNumpyImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    force_numpy=True,
):
    """Sub Function -- Numpy implementation."""

    pass


def Sub(size, dtype, accuracy=None):
    """Sub Function."""
    return (
        _SubIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if 3 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _SubNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Sub._ipps_candidates = _SubIPPSImpl._ipps_candidates


class _SubIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Sub_I Function."""

    pass


class _SubINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    force_numpy=True,
):
    """Sub_I Function."""

    pass


def Sub_I(size, dtype, accuracy=None):
    """Sub_I Function."""
    return (
        _SubIIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.complex128,)
        or accuracy is not None
        else _SubINumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Sub_I._ipps_candidates = _SubIIPPSImpl._ipps_candidates


class _SubRevIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    numpy_swap=True,
    reverse=True,
):
    """SubRev_I Function -- Intel IPPS implementation."""

    pass


class _SubRevINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    numpy_swap=True,
    reverse=True,
    force_numpy=True,
):
    """SubRev_I Function -- Numpy implementation."""

    pass


def SubRev_I(size, dtype, accuracy=None):
    """SubRev_I Function."""
    return (
        _SubRevIIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.complex128,)
        or accuracy is not None
        else _SubRevINumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


SubRev_I._ipps_candidates = _SubRevIIPPSImpl._ipps_candidates


class _MulIPPSImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Mul Function."""

    pass


class _MulNumpyImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
    force_numpy=True,
):
    """Mul Function."""

    pass


def Mul(dtype, accuracy=None, size=None):
    """Mul Function."""
    return (
        _MulIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex128,) or accuracy is not None
        else _MulNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Mul._ipps_candidates = _MulIPPSImpl._ipps_candidates


class Mul_I(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
    candidates=numpy_ipps.policies.no_complex_candidates,
    accuracies=(numpy_ipps.policies.Accuracy.LEVEL_3,),
):
    """Mul_I Function."""

    pass


class _DivIPPSImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
):
    """Div Function -- Intel IPPS implementation."""

    pass


class _DivNumpyImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    force_numpy=True,
):
    """Div Function -- Numpy implementation."""

    pass


def Div(dtype, accuracy=None, size=None):
    """Div Function."""
    if accuracy is not None:
        if dtype == _numpy.complex128:
            return _DivNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
        elif 3 * size * _numpy.dtype(
            dtype
        ).itemsize < numpy_ipps.support.L1 or _numpy.dtype(
            dtype
        ).itemsize not in (
            8,
        ):
            return _DivIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        return _DivNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    else:
        return _DivIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)


Div._ipps_candidates = _DivIPPSImpl._ipps_candidates


class _DivIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    candidates=numpy_ipps.policies.no_complex_candidates,
):
    """Div_I Function."""

    pass


class _DivINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    candidates=numpy_ipps.policies.no_complex_candidates,
    force_numpy=True,
):
    """Div_I Function."""

    pass


def Div_I(dtype, accuracy=None, size=None):
    """Div_I Function."""
    return (
        _DivIIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if 2 * size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.float64,)
        or accuracy is not None
        else _DivINumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Div_I._ipps_candidates = _DivIIPPSImpl._ipps_candidates


class _DivRevIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    numpy_swap=True,
    reverse=True,
):
    """DivRev_I Function -- Intel IPPS implementation."""

    pass


class _DivRevINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Div",
    numpy_backend=_numpy.divide,
    numpy_swap=True,
    reverse=True,
    force_numpy=True,
):
    """DivRev_I Function -- Numpy implementation."""

    pass


def DivRev_I(dtype, accuracy=None, size=None):
    """DivRev_I Function."""
    return (
        _DivRevIIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex128,) or accuracy is not None
        else _DivRevINumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


DivRev_I._ipps_candidates = _DivRevIIPPSImpl._ipps_candidates


class _PowIPPSImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Pow",
    numpy_backend=_numpy.power,
):
    """Pow Function -- Intel IPPS implementation."""

    pass


class _PowNumpyImpl(
    metaclass=_binaries.BinaryAccuracy,
    ipps_backend="Pow",
    numpy_backend=_numpy.power,
    force_numpy=True,
):
    """Pow Function -- Numpy implementation."""

    pass


def Pow(dtype, accuracy=None, size=None):
    """Pow Function."""
    return (
        _PowIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if dtype not in (_numpy.complex64, _numpy.complex128)
        or accuracy is not None
        else _PowNumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


Pow._ipps_candidates = _PowIPPSImpl._ipps_candidates


class _PowRevIIPPSImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Pow",
    numpy_backend=_numpy.power,
    numpy_swap=True,
    reverse=True,
):
    """PowRev_I Function -- Intel IPPS implementation."""

    pass


class _PowRevINumpyImpl(
    metaclass=_binaries.BinaryAccuracy_I,
    ipps_backend="Pow",
    numpy_backend=_numpy.power,
    numpy_swap=True,
    reverse=True,
    force_numpy=True,
):
    """PowRev_I Function -- Numpy implementation."""

    pass


def PowRev_I(size, dtype, accuracy=None):
    """PowRev_I Function."""
    return (
        _PowRevIIPPSImpl(dtype=dtype, accuracy=accuracy, size=size)
        if size * _numpy.dtype(dtype).itemsize < numpy_ipps.support.L1
        or dtype not in (_numpy.float32, _numpy.float64, _numpy.complex128)
        or accuracy is not None
        else _PowRevINumpyImpl(dtype=dtype, accuracy=accuracy, size=size)
    )


PowRev_I._ipps_candidates = _PowRevIIPPSImpl._ipps_candidates

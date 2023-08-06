import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps
import numpy_ipps.fft


cache_L1 = numpy.min(
    [cache_size for _u0, _u1, cache_size in numpy_ipps.support.cache_params()]
)
orders = (
    8,
    int(numpy.ceil(numpy.log2(cache_L1))),
)
dtypes = (
    numpy.complex64,
    numpy.complex128,
)
dtypes_fir = (
    numpy.float32,
    numpy.float64,
    numpy.complex64,
    numpy.complex128,
)


unary_classes = (
    numpy_ipps.FFTFwd,
    numpy_ipps.FFTInv,
)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_fft.log",
    )
    ch = logging.FileHandler(log_file, mode="w")
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(ch)
    importlib.reload(numpy_ipps)

    yield logger

    logger.removeHandler(ch)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes + (numpy.float32, numpy.float64))
@pytest.mark.parametrize("feature", unary_classes)
def test_ipps_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(order=order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unary_classes)
def test_numpy_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(order=order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_fir)
def test_ipps_FIRDirect(logger_fixture, benchmark, order, dtype):
    kernel = (1 + numpy.random.rand(8)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.fft._FIR_Direct(kernel=kernel, method=0x00000001)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_fir)
def test_numpy_FIRDirect(logger_fixture, benchmark, order, dtype):
    kernel = (1 + numpy.random.rand(8)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.fft._FIR_Direct(kernel=kernel, method=0x00000001)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_fir)
def test_ipps_FIRDirectFFT(logger_fixture, benchmark, order, dtype):
    kernel = (1 + numpy.random.rand(8)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.fft._FIR_Direct(kernel=kernel, method=0x00000002)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_fir)
def test_numpy_FIRDirectFFT(logger_fixture, benchmark, order, dtype):
    kernel = (1 + numpy.random.rand(8)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.fft._FIR_Direct(kernel=kernel, method=0x00000002)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (4, 6, 8, 10, 12, 14, 16))
@pytest.mark.parametrize("dtype", (numpy.complex64, numpy.complex128))
def test_ipps_fir_fftC(logger_fixture, benchmark, order, kernel_size, dtype):
    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.fft._FIR_FFT_C(kernel=kernel, order=order)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (4, 6, 8, 10, 12, 14, 16))
@pytest.mark.parametrize("dtype", (numpy.float32, numpy.float64))
def test_ipps_fir_fftR(logger_fixture, benchmark, order, kernel_size, dtype):
    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.fft._FIR_FFT_R(kernel=kernel, order=order)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (4, 6, 8, 10, 12, 14, 16))
@pytest.mark.parametrize(
    "dtype", (numpy.float32, numpy.float64, numpy.complex64, numpy.complex128)
)
def test_ipps_fir_direct(logger_fixture, benchmark, order, kernel_size, dtype):
    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.fft._FIR_Direct(kernel=kernel, method=0x00000001)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


@pytest.mark.parametrize("order", (6, 8, 10, 12, 14, 16, 18, 20))
@pytest.mark.parametrize("kernel_size", (4, 6, 8, 10, 12, 14, 16))
@pytest.mark.parametrize(
    "dtype", (numpy.float32, numpy.float64, numpy.complex64, numpy.complex128)
)
def test_ipps_fir_directFFT(
    logger_fixture, benchmark, order, kernel_size, dtype
):
    kernel = (1 + numpy.random.rand(kernel_size)).astype(dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    feature_obj = numpy_ipps.fft._FIR_Direct(kernel=kernel, method=0x00000002)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)

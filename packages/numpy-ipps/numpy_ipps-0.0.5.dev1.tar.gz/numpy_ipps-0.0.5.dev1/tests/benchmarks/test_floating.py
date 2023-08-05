import importlib
import logging
import os

import numpy
import pytest

import numpy_ipps


cache_L1 = numpy.min(
    [cache_size for _u0, _u1, cache_size in numpy_ipps.support.cache_params()]
)
orders = (
    6,
    int(numpy.ceil(numpy.log2(cache_L1))),
)
dtypes = (
    numpy.float32,
    numpy.float64,
    numpy.complex64,
    numpy.complex128,
)
if (
    "NUMPY_IPPS_FAST_TEST" in os.environ
    and os.environ["NUMPY_IPPS_FAST_TEST"] == "ON"
):
    dtypes = (numpy.float32,)


binary_classes = (
    numpy_ipps.Div,
    numpy_ipps.Pow,
)
binaryI_classes = (
    numpy_ipps.Div_I,
    numpy_ipps.DivRev_I,
    numpy_ipps.PowRev_I,
)

binaryL3_classes = (
    numpy_ipps.Add,
    numpy_ipps.Sub,
    numpy_ipps.Mul,
)
binaryL3I_classes = (
    numpy_ipps.Add_I,
    numpy_ipps.Sub_I,
    numpy_ipps.SubRev_I,
    numpy_ipps.Mul_I,
)

unary_classes = (
    numpy_ipps.Sqrt,
    numpy_ipps.Cbrt,
)
unaryI_classes = (
    numpy_ipps.Sqrt_I,
    numpy_ipps.Cbrt_I,
)

unaryL3_classes = (
    numpy_ipps.Sqr,
    numpy_ipps.Abs,
)
unaryL3I_classes = (
    numpy_ipps.Sqr_I,
    numpy_ipps.Abs_I,
)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_complex.log",
    )
    ch = logging.FileHandler(log_file, mode="w")
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(ch)
    importlib.reload(numpy_ipps)

    yield logger

    logger.removeHandler(ch)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binary_classes)
def test_ipps_binary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src1 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src2 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst, dst_ref):
        benchmark(feature_obj, src1, src2, dst)
        feature_obj._numpy_backend(src1, src2, dst_ref)

    numpy.testing.assert_array_almost_equal_nulp(dst, dst_ref, nulp=5)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryI_classes)
def test_ipps_binaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(feature_obj, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binary_classes)
def test_numpy_binary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src1 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src2 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(feature_obj._numpy_backend, src1, src2, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryI_classes)
def test_numpy_binaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(feature_obj._numpy_backend, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryL3_classes)
def test_ipps_binaryL3(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src1 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src2 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst, dst_ref):
        benchmark(feature_obj, src1, src2, dst)
        feature_obj._numpy_backend(src1, src2, dst_ref)

    numpy.testing.assert_array_almost_equal_nulp(dst, dst_ref, nulp=5)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryL3I_classes)
def test_ipps_binaryL3I(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(
        size=1 << order,
        dtype=dtype,
    )
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(feature_obj, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryL3_classes)
def test_numpy_binaryL3(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(
        size=1 << order,
        dtype=dtype,
    )
    src1 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src2 = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(feature_obj._numpy_backend, src1, src2, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", binaryL3I_classes)
def test_numpy_binaryL3I(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(
        size=1 << order,
        dtype=dtype,
    )
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(feature_obj._numpy_backend, src, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unary_classes)
def test_ipps_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)
        feature_obj._numpy_backend(src, dst_ref)

    numpy.testing.assert_array_almost_equal_nulp(dst, dst_ref, nulp=5)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unaryI_classes)
def test_ipps_unaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unary_classes)
def test_numpy_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unaryI_classes)
def test_numpy_unaryI(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj._numpy_backend, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unaryL3_classes)
def test_ipps_unaryL3(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(
        size=1 << order,
        dtype=dtype,
    )
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)
    dst_ref = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst, dst_ref):
        benchmark(feature_obj, src, dst)
        feature_obj._numpy_backend(src, dst_ref)

    numpy.testing.assert_array_almost_equal_nulp(dst, dst_ref, nulp=5)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unaryL3I_classes)
def test_ipps_unaryL3I(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(
        size=1 << order,
        dtype=dtype,
    )
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj, src_dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unaryL3_classes)
def test_numpy_unaryL3(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(
        size=1 << order,
        dtype=dtype,
    )
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj._numpy_backend, src, dst)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes)
@pytest.mark.parametrize("feature", unaryL3I_classes)
def test_numpy_unaryL3I(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(
        size=1 << order,
        dtype=dtype,
    )
    src_dst = (1 + numpy.random.rand(1 << order)).astype(dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(feature_obj._numpy_backend, src_dst)

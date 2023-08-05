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
)
if (
    "NUMPY_IPPS_FAST_TEST" in os.environ
    and os.environ["NUMPY_IPPS_FAST_TEST"] == "ON"
):
    dtypes = (numpy.float32,)

unary_classes = (
    numpy_ipps.Erf,
    numpy_ipps.Erfc,
    numpy_ipps.ErfInv,
    numpy_ipps.ErfcInv,
    numpy_ipps.CdfNorm,
    numpy_ipps.CdfNormInv,
)
unaryI_classes = (
    numpy_ipps.ErfInv_I,
    numpy_ipps.CdfNormInv_I,
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
@pytest.mark.parametrize("feature", unary_classes)
def test_ipps_unary(logger_fixture, benchmark, order, dtype, feature):
    if dtype not in feature._ipps_candidates:
        return

    feature_obj = feature(size=1 << order, dtype=dtype)
    src = (1 + numpy.random.rand(1 << order)).astype(dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(feature_obj, src, dst)


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

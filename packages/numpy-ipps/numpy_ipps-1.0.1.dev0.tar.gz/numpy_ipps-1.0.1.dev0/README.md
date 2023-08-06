## Introduction

Numpy Intel IPP Signal is a Python wrapper for Intel IPP Signal functions.

## Principles

Numpy Intel IPP Signal is based on a __Setup__ and __Payoff__ strategy
* __Setup__ : First Numpy data buffers and Intel IPP Signal operations are setup,
this step can be slow.
* __Payoff__ : Then operations are executed as fast as possible with Intel IPP Signal
or Numpy backend functions.

## Example

```python
# Two Numpy data buffers
src1 = numpy.ones(100, dtype=numpy.float32)
src2 = numpy.zeros(100, dtype=numpy.float32)

# A result buffer
dst = numpy.empty(100, dtype=numpy.float32)

# Intel IPP Signal Add operation
add = numpy_ipps.Add(dtype=numpy.float32)

# Unpack Numpy buffer for fast access
with numpy_ipps.utils.context(src1, src2, dst):
    add(src1, src2, dst)  # Fast addition: dst[n] <- src1[n] + src2[n]
```

See more details at [ReadTheDocs.io](https://numpy-intel-ipp-signal.readthedocs.io/).

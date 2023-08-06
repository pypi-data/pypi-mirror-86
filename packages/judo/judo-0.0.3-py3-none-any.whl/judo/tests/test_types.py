import numpy
import pytest
import torch

import judo
from judo.tests.test_backend import backend


class TestDataTypes:
    def test_bool(self, backend):
        backend.set_backend("numpy")
        assert judo.bool == numpy.bool_, judo.bool
        backend.set_backend("torch")
        assert judo.bool == torch.bool

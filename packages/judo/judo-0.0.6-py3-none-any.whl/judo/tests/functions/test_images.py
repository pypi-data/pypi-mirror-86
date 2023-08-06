import pytest

import judo
from judo import API, random_state


class TestImages:
    @pytest.mark.parametrize("size", [(64, 64, 3), (21, 73, 3), (70, 20, 3)])
    def test_resize_frame_rgb(self, size):
        random_state.seed(160290)
        frame = random_state.randint(0, 255, size=size, dtype=judo.uint8)
        resized = API.resize_image(frame, width=size[1], height=size[0], mode="RGB")
        assert size == resized.shape

    @pytest.mark.parametrize("size", [(64, 64), (21, 73), (70, 2)])
    def test_resize_frame_grayscale(self, size):
        random_state.seed(160290)
        frame = random_state.randint(0, 255, size=size + (3,), dtype=judo.uint8)
        resized = API.resize_image(frame, size[1], size[0], "L")
        assert size == resized.shape

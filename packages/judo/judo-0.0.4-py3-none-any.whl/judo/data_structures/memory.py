import logging
from typing import Dict, Iterable, List, Tuple, Union

import judo
from judo.functions import random_state
from judo.judo_backend import Backend
from judo.typing import Tensor


class ReplayMemory:
    """Replay buffer that contains data collected from algorithm runs."""

    _log = logging.getLogger("Memory")

    def __init__(
        self, max_size: int, names: Union[List[str], Tuple[str]], min_size: int = None,
    ):
        """
        Initialize a :class:`ReplayMemory`.

        Args:
            max_size: Maximum number of experiences that will be stored.
            names: Names of the replay data attributes that will be stored.
            min_size: Minimum number of samples that need to be stored before the \
                     replay memory is considered ready. If ``None`` it will be equal \
                     to max_size.

        """
        self.max_size = max_size
        self.min_size = 1.0 if min_size is None else min_size
        self.names = names
        self.reset()

    def __len__(self) -> int:
        first_attr = getattr(self, self.names[0])
        return 0 if first_attr is None else len(first_attr)

    def __repr__(self) -> str:
        text = "Memory with min_size %s max_size %s and length %s" % (
            self.min_size,
            self.max_size,
            len(self),
        )
        return text

    def reset(self):
        """Delete all the data previously stored in the memory."""
        for name in self.names:
            setattr(self, name, None)

    def get(self, name):
        """Get attributes of the memory."""
        if name == "len":
            return len(self)
        return getattr(self, name)

    def is_ready(self) -> bool:
        """
        Return ``True`` if the number of experiences in the memory is greater than ``min_size``.
        """
        return len(self) >= self.min_size

    def get_values(self) -> Tuple[Tensor, ...]:
        """Return a tuple containing the memorized data for all the saved data attributes."""
        return tuple([getattr(self, val) for val in self.names])

    def as_dict(self) -> Dict[str, Tensor]:
        return dict(zip(self.names, self.get_values()))

    def iterate_batches(self, batch_size: int, as_dict: bool = True):
        with Backend.use_backend("numpy"):
            indexes = random_state.permutation(range(len(self)))
            for i in range(0, len(self), batch_size):
                batch_ix = indexes[i : i + batch_size]
                data = tuple([getattr(self, val)[batch_ix] for val in self.names])
                if as_dict:
                    yield dict(zip(self.names, data))
                else:
                    yield data

    def iterate_values(self, randomize: bool = False) -> Iterable[Tuple[Tensor]]:
        """
        Return a generator that yields a tuple containing the data of each state \
        stored in the memory.
        """
        indexes = range(len(self))
        if randomize:
            with Backend.use_backend("numpy"):
                indexes = random_state.permutation(indexes)
        for i in indexes:
            yield tuple([getattr(self, val)[i] for val in self.names])

    def append(self, **kwargs):
        for name, val in kwargs.items():
            if name not in self.names:
                raise KeyError("%s not in self.names: %s" % (name, self.names))
            # Scalar vectors are transformed to columns
            val = judo.to_backend(val)
            if len(val.shape) == 0:
                val = judo.unsqueeze(val)
            if len(val.shape) == 1:
                val = val.reshape(-1, 1)
            try:
                processed = (
                    val
                    if getattr(self, name) is None
                    else judo.concatenate([getattr(self, name), val])
                )
                if len(processed) > self.max_size:
                    processed = processed[: self.max_size]
            except Exception as e:
                print(name, val.shape, getattr(self, name).shape)
                raise e
            setattr(self, name, processed)
        self._log.info("Memory now contains %s samples" % len(self))

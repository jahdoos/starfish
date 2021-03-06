import os
from tempfile import TemporaryDirectory

import numpy as np
import pytest

from starfish import ImageStack
from starfish.core.types import Features
from ..intensity_table import IntensityTable


def test_to_mermaid_dataframe():
    """
    Creates a basic IntensityTable from an ImageStack and verifies that it can be dumped to disk
    as a DataFrame which MERmaid can load. Does not explicitly load the DataFrame in MERmaid.

    Verifies that the save function throws an error when target assignments are not present, which
    are required by MERmaid.
    """
    r, c, z, y, x = 1, 5, 2, 2, 5
    data = np.zeros(100, dtype=np.float32).reshape(r, c, z, y, x)
    image_stack = ImageStack.from_numpy(data)
    intensities = IntensityTable.from_image_stack(image_stack)

    # without a target assignment, should raise RuntimeError.
    with pytest.raises(RuntimeError):
        with TemporaryDirectory() as dir_:
            intensities.to_mermaid(os.path.join(dir_, 'test.csv.gz'))

    # assign targets
    intensities[Features.TARGET] = (Features.AXIS, np.random.choice(list('ABCD'), size=20))
    intensities[Features.DISTANCE] = (Features.AXIS, np.random.rand(20))
    with TemporaryDirectory() as dir_:
        intensities.to_mermaid(os.path.join(dir_, 'test.csv.gz'))

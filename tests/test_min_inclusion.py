from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pytest

import gdsfactory as gf
from gdsfactory.geometry import check_inclusion

if TYPE_CHECKING:
    from gdsfactory.component import Component


@gf.cell
def component_min_inclusion(
    inclusion: float,
    width: float = 0.5,
    layer1: tuple[int, int] = (1, 0),
    layer2: tuple[int, int] = (2, 0),
) -> Component:
    c = gf.Component()
    r1 = c << gf.components.rectangle(size=(width, width), layer=layer1)
    r2 = c << gf.components.rectangle(
        size=(width - 2 * inclusion, width - 2 * inclusion),
        layer=layer2,
    )
    r1.x = 0
    r1.y = 0
    r2.x = 0
    r2.y = 0
    return c


@pytest.mark.parametrize(
    ("inclusion", "min_inclusion", "area_expected"),
    [(0.1, 0.11, 16e4), (0.1, 0.01, 0)],
)
def test_inclusion(inclusion: float, min_inclusion: float, area_expected: int) -> None:
    c = component_min_inclusion(inclusion=inclusion)
    area = check_inclusion(c, min_inclusion=min_inclusion)
    assert np.isclose(area, area_expected)


if __name__ == "__main__":
    test_inclusion(0.1, 0.01, 0)

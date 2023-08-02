from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import gdsfactory as gf
from gdsfactory.difftest import difftest

if TYPE_CHECKING:
    from pytest_regressions.data_regression import DataRegressionFixture

sequences = ["ABHBA", "!HH", "AB", "HH!", "H"]


@pytest.mark.parametrize("index", range(len(sequences)))
def test_component_from_sequence(
    index: int,
    data_regression: DataRegressionFixture,
    check: bool = True,
) -> None:
    bend180 = gf.components.bend_circular180()
    wg_pin = gf.components.straight_pin(length=40)
    wg = gf.components.straight()

    # Define a map between symbols and (component, input port, output port)
    symbol_to_component_map = {
        "A": (bend180, "o1", "o2"),
        "B": (bend180, "o2", "o1"),
        "H": (wg_pin, "o1", "o2"),
        "-": (wg, "o1", "o2"),
    }

    sequence = sequences[index]
    c = gf.components.component_sequence(
        sequence=sequence,
        symbol_to_component=symbol_to_component_map,
    )

    difftest(c)
    if check:
        data_regression.check(c.to_dict())


if __name__ == "__main__":
    test_component_from_sequence(1, None, False)

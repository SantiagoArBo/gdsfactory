from __future__ import annotations

from typing import TYPE_CHECKING

import gdsfactory as gf

if TYPE_CHECKING:
    from pytest_regressions.data_regression import DataRegressionFixture


def test_get_bundle_electrical_multilayer(
    data_regression: DataRegressionFixture,
    check: bool = True,
) -> None:
    lengths = {}
    c = gf.Component("multi-layer")
    columns = 2
    ptop = c << gf.components.pad_array(columns=columns)
    pbot = c << gf.components.pad_array(orientation=90, columns=columns)

    ptop.movex(300)
    ptop.movey(300)
    routes = gf.routing.get_bundle_electrical_multilayer(
        ptop.ports,
        pbot.ports,
        end_straight_length=100,
        separation=20,
    )

    for i, route in enumerate(routes):
        c.add(route.references)
        lengths[i] = route.length

    if check:
        data_regression.check(lengths)


if __name__ == "__main__":
    test_get_bundle_electrical_multilayer(None, check=False)

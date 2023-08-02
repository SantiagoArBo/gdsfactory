from __future__ import annotations

from typing import TYPE_CHECKING

import gdsfactory as gf

if TYPE_CHECKING:
    from pytest_regressions.data_regression import DataRegressionFixture


def test_get_bundle_u_direct_different_x(
    data_regression: DataRegressionFixture,
    check: bool = True,
) -> None:
    """ """

    c = gf.Component("test_get_bundle_u_direct_different_x")
    w = c << gf.components.straight_array(n=4, spacing=200)
    d = c << gf.components.nxn(west=4, east=0, north=0, south=0)
    d.y = w.y
    d.xmin = w.xmax + 200

    ports1 = w.get_ports_list(orientation=0)
    ports2 = d.get_ports_list(orientation=0)

    ports1 = [
        w.ports["o7"],
        w.ports["o8"],
    ]
    ports2 = [
        d.ports["o2"],
        d.ports["o1"],
    ]

    routes = gf.routing.get_bundle(ports1, ports2)

    lengths = {}
    for i, route in enumerate(routes):
        c.add(route.references)
        lengths[i] = route.length

    if check:
        data_regression.check(lengths)


if __name__ == "__main__":
    test_get_bundle_u_direct_different_x(None, check=False)

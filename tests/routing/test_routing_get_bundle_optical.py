from __future__ import annotations

from pytest_regressions.data_regression import DataRegressionFixture

import gdsfactory as gf


def test_get_bundle_optical(
    data_regression: DataRegressionFixture, check: bool = True
) -> None:
    lengths = {}

    c = gf.Component()

    w = c << gf.components.straight_array(n=4, spacing=200)
    d = c << gf.components.nxn(west=4, east=0)
    d.y = w.y
    d.xmin = w.xmax + 200

    ports1 = [
        w.ports["o7"],
        w.ports["o8"],
    ]
    ports2 = [
        d.ports["o2"],
        d.ports["o1"],
    ]

    routes = gf.routing.get_bundle(ports1, ports2, sort_ports=True, radius=10)
    for i, route in enumerate(routes):
        c.add(route.references)
        lengths[i] = route.length

    if check:
        data_regression.check(lengths)


def test_get_bundle_optical2(
    data_regression: DataRegressionFixture, check: bool = True
) -> None:
    lengths = {}

    c = gf.Component()
    w = c << gf.components.straight_array(n=4, spacing=200)
    d = c << gf.components.nxn(west=4, east=1)
    d.y = w.y
    d.xmin = w.xmax + 200

    ports1 = w.get_ports_list(orientation=0)
    ports2 = d.get_ports_list(orientation=180)

    routes = gf.routing.get_bundle(ports1, ports2, sort_ports=True)

    for i, route in enumerate(routes):
        c.add(route.references)
        lengths[i] = route.length

    if check:
        data_regression.check(lengths)


if __name__ == "__main__":
    # test_get_bundle_optical(None, check=False)
    test_get_bundle_optical2(None, check=False)

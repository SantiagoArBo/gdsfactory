from __future__ import annotations

import gdsfactory as gf


def test_netlist_with_routes() -> None:
    """Tests netlist with routes."""
    c = gf.Component()
    w = c << gf.components.straight(length=3)
    b = c << gf.components.bend_circular()
    w.xmax = 0
    b.xmin = 10

    routes = gf.routing.get_bundle(w.ports["o2"], b.ports["o1"])
    for route in routes:
        c.add(route.references)
    n = c.get_netlist()
    connections = n["connections"]

    assert len(c.get_dependencies()) == 3
    assert len(connections) == 2  # 2 components + 1 flat netlist


if __name__ == "__main__":
    c = test_netlist_with_routes()
    c.show(show_ports=True)

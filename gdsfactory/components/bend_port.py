from __future__ import annotations

from typing import TYPE_CHECKING

import gdsfactory as gf
from gdsfactory.components.bend_circular import bend_circular
from gdsfactory.components.straight_heater_metal import straight_heater_metal

if TYPE_CHECKING:
    from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell
def bend_port(
    component: ComponentSpec = straight_heater_metal,
    port_name: str = "l_e1",
    port_name2: str = "r_e1",
    port_name1_bend: str | None = None,
    port_name2_bend: str | None = None,
    cross_section: CrossSectionSpec = "metal3_with_bend",
    bend: ComponentSpec = bend_circular,
    angle: float = 180,
    extension_length: float | None = None,
    **kwargs,
) -> gf.Component:
    """Returns a component with a bend and a straight extension.

    Args:
    ----
        component: to bend.
        port_name: of the component port origin.
        port_name2: of the component port destination.
        port_name1_bend: for bend port.
        port_name2_bend: for bend port.
        cross_section: for the bend.
        bend: factory for the bend.
        angle: for the bend.
        extension_length: for the straight after the bend.
        kwargs: cross_section settings.
    """
    c = gf.Component()
    component = gf.get_component(component)
    c.component = component

    if port_name not in component.ports:
        msg = f"port_name {port_name!r} not in {list(component.ports.keys())}"
        raise ValueError(
            msg,
        )

    extension_length = extension_length or abs(
        component.ports[port_name2].center[0] - component.ports[port_name].center[0],
    )

    ref = c << component
    b = c << gf.get_component(bend, angle=angle, cross_section=cross_section, **kwargs)
    bend_ports = b.get_ports_list()

    port_name1_bend = port_name1_bend or bend_ports[0].name
    port_name2_bend = port_name2_bend or bend_ports[1].name

    b.connect(port_name1_bend, ref.ports[port_name])

    s = c << gf.components.straight(
        length=extension_length,
        cross_section=cross_section,
        **kwargs,
    )
    straight_ports = s.get_ports_list()
    o2 = straight_ports[1].name
    o1 = straight_ports[0].name
    s.connect(o2, b.ports[port_name2_bend])

    c.add_ports(ref.get_ports_list())
    c.ports.pop(port_name)
    c.add_port(port_name, port=s.ports[o1])
    c.copy_child_info(component)
    return c


if __name__ == "__main__":
    c = bend_port()
    c.show(show_ports=True)

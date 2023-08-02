from __future__ import annotations

from typing import TYPE_CHECKING

import gdsfactory as gf

if TYPE_CHECKING:
    from gdsfactory.component import Component


@gf.cell
def component_with_label_float() -> Component:
    c = gf.Component("component_with_label_float")
    c << gf.components.rectangle()
    c.add_label(text="demo", position=(0.0, 0.0), layer=gf.LAYER.TEXT)
    return c


@gf.cell
def component_with_label_int() -> Component:
    c = gf.Component("component_with_label_int")
    c << gf.components.rectangle()
    c.add_label(text="demo", position=(0, 0), layer=gf.LAYER.TEXT)
    return c


def test_move_float_with_int() -> None:
    c = gf.Component("test_move_float_with_int")
    ref = c.add_ref(component_with_label_float())
    ref.movex(10)


def test_move_int_with_float() -> None:
    c = gf.Component("test_move_float_with_float")
    ref = c.add_ref(component_with_label_int())
    ref.movex(10)


if __name__ == "__main__":
    test_move_float_with_int()

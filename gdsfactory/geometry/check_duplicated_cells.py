from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def check_duplicated_cells(gdspath: Path | str):
    """Reads cell and checks for duplicated cells.

    klayout will fail to load the layout if it finds any duplicated cells.

    Args:
    ----
        gdspath: path to GDS or Component

    """
    import klayout.db as pya

    from gdsfactory.component import Component

    if isinstance(gdspath, Component):
        gdspath.flatten()
        gdspath = gdspath.write_gds()
    layout = pya.Layout()
    layout.read(str(gdspath))
    return layout.top_cell()

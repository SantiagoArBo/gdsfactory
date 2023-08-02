from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from gdsfactory.config import __version__

if TYPE_CHECKING:
    from gdsfactory.component import Component


def grating_coupler(gc: Component) -> None:
    if not gc.info.get("polarization"):
        msg = f"{gc.name} does not have polarization"
        raise ValueError(msg)

    if gc.info.get("polarization") not in ["te", "tm", "dual"]:
        msg = f"{gc.name} polarization not 'te' or 'tm' or 'dual"
        raise ValueError(msg)

    if not gc.info.get("wavelength"):
        msg = f"{gc.name} wavelength does not have wavelength"
        raise ValueError(msg)
    if not (0.5 < gc.info["wavelength"] < 5.0):
        msg = f"{gc.name} wavelength {gc.wavelength} should be in um"
        raise ValueError(msg)

    if "o1" not in gc.ports:
        warnings.warn(
            f"grating_coupler {gc.name} should have a o1 port. It has {gc.ports}",
            stacklevel=3,
        )
    if "o1" in gc.ports and gc.ports["o1"].orientation != 180:
        warnings.warn(
            f"grating_coupler {gc.name} orientation = {gc.ports['o1'].orientation}"
            " should be 180 degrees",
            stacklevel=3,
        )


def version(
    requirement: str,
    current: str = __version__,
    package_name="gdsfactory",
) -> None:
    """Raises error if current version does not match requirement."""
    try:
        import semantic_version
    except ModuleNotFoundError:
        print("You need to 'pip install semantic-version'")
        raise

    s = semantic_version.SimpleSpec(requirement)
    if not s.match(semantic_version.Version(current)):
        msg = f"{package_name} requirement {requirement}\nnot compatible your current installed version {current}\nyou can run:\npip install {package_name} {requirement}\n"
        raise ValueError(
            msg,
        )


if __name__ == "__main__":
    version("<=3.8.7")

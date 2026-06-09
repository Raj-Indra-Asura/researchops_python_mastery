"""Sanity test — verifies the package is importable and basic version info works."""

import researchops


def test_package_importable() -> None:
    """The researchops package must import without errors."""
    assert researchops is not None


def test_version_defined() -> None:
    """The package must have a __version__ attribute."""
    assert hasattr(researchops, "__version__")
    assert isinstance(researchops.__version__, str)
    assert researchops.__version__ != ""

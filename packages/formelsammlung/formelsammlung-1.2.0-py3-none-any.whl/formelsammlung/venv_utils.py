"""
    formelsammlung.venv_utils
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Utility function for working with virtual environments.

    :copyright: 2020 (c) Christian Riedel
    :license: GPLv3, see LICENSE file for more details
"""  # noqa: D205, D208, D400
import os
import shutil
import sys

from pathlib import Path
from typing import Optional, Tuple, Union


def get_venv_path() -> Optional[str]:
    """Get path to the venv from where the python executable runs.

    :return: Return venv path or None if python is not called from a venv.
    """
    if hasattr(sys, "real_prefix"):
        return sys.real_prefix  # type: ignore[no-any-return,attr-defined] # pylint: disable=E1101
    if sys.base_prefix != sys.prefix:
        return sys.prefix
    return None


def get_venv_site_packages_dir(venv_path: Union[str, Path]) -> Path:
    """Return path to site-packages dir of given venv.

    :param venv_path: Path to venv
    :return: Path to site-packages dir
    """
    return list(Path(venv_path).glob("**/site-packages"))[0]


def where_installed(program: str) -> Tuple[int, Optional[str], Optional[str]]:
    """Find installation locations for given program.

    Return exit code and locations based on found installation places.
    Search in current venv and globally.

    Exit codes:

    - 0 = nowhere
    - 1 = venv
    - 2 = global
    - 3 = both

    :param program: Program to search
    :return: Exit code, venv executable path, glob executable path
    """
    exit_code = 0

    exe = shutil.which(program)
    if not exe:
        return exit_code, None, None

    venv_path = get_venv_path()
    bin_dir = "\\Scripts" if sys.platform == "win32" else "/bin"
    path_wo_venv = os.environ["PATH"].replace(f"{venv_path}{bin_dir}", "")
    glob_exe = shutil.which(program, path=path_wo_venv)

    if glob_exe is None:
        exit_code += 1
    elif exe == glob_exe:
        exit_code += 2
        exe = None
    else:
        exit_code += 3
    return exit_code, exe, glob_exe

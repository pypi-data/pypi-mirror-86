"""
    formelsammlung.tox_env_exe_runner
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Call tools from tox environments.

    :copyright: 2020 (c) Christian Riedel
    :license: GPLv3, see LICENSE file for more details
"""  # noqa: D205, D208, D400
import subprocess  # nosec
import sys

from pathlib import Path
from typing import List, Optional


def env_exe_runner(
    runner: str, envs: List[str], tool: str, tool_args: Optional[List[str]] = None
) -> int:
    """Call given ``tool`` from given ``tox`` or ``nox`` env considering OS.

    :param runner: 'nox' or 'tox'
    :param envs: List of environments to search the ``tool`` in.
    :param tool: Name of the executable to run.
    :param tool_args: Arguments to give to the ``tool``.
    :return: Exit code 127 if no executable is found or the exit code of the called cmd.
    """
    if runner not in ("tox", "nox"):
        print("No valid runner was given. Choose either 'tox' or 'nox'.")
        return 127

    is_win = sys.platform == "win32"

    exe = Path(f"Scripts/{tool}.exe") if is_win else Path(f"bin/{tool}")
    cmd = None

    if not tool_args:
        tool_args = []

    for env in envs:
        path = Path(f".{runner}") / env / exe
        if path.is_file():
            cmd = (str(path), *tool_args)

    if cmd is None:
        print(
            f"No '{tool}' executable found. Make sure one of the "
            f"following `{runner}` envs is accessible: {envs}"
        )
        return 127

    return subprocess.call(cmd)  # nosec


def cli_caller() -> int:
    """Warp ``env_exe_runner`` to be callable by cli.

    Script to call executables in `tox`/`nox` envs considering OS.

    The script takes two mandatory arguments:

    1. The runner managing the env: `tox` or `nox`.
    2. A string with comma separated `tox`/`nox` envs to check for the executable.
       The envs are checked in given order.
    3. The executable to call like e.g. `pylint`.

    All other arguments after are passed to the tool on call.

    :return: Exit code from ``env_exe_runner``
    """
    return env_exe_runner(
        sys.argv[1], sys.argv[2].split(","), sys.argv[3], sys.argv[4:]
    )  # pragma: no cover


if __name__ == "__main__":
    sys.exit(cli_caller())

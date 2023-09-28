from typing import Optional

from wmtools.core.command import CommandRunner, run_command


def read_password(folder: str, key: str, command_runner: CommandRunner = run_command) -> Optional[str]:
    return command_runner(["secret-tool", "lookup", folder, key]).stdout or None


def ask_password(command_runner: CommandRunner = run_command) -> Optional[str]:
    result = command_runner(["zenity", "--password"])
    if result.returncode:
        return None
    return result.stdout


def save_password(folder: str, key: str, password: str, label: str, command_runner: CommandRunner = run_command) -> None:
    command_runner(["secret-tool", "store", "--label", label, folder, key], input=password)

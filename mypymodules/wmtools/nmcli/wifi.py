from dataclasses import dataclass
from typing import List

from wmtools.core.command import CommandRunner, run_command
from wmtools.nmcli.tools import nmcli_output_reader


@dataclass
class WifiConn:
    ssid: str
    bar: str
    active: bool
    security: bool


def scan(command_runner: CommandRunner = run_command) -> List[WifiConn]:
    fields = "ssid,bars,active,security"
    scan_result = command_runner([
        "nmcli", 
        f"--fields={fields}", 
        "--terse",
        "device",
        "wifi",
        "list"
    ])
    networks = []
    for item in nmcli_output_reader(scan_result.stdout, fields):
        if not item["ssid"]:
            continue
        networks.append(WifiConn(
            ssid=item["ssid"],
            bar=item["bars"],
            active=item["active"] == 'yes',
            security=bool(item["security"]),
        ))
    return networks


def connect(name: str, command_runner: CommandRunner = run_command) -> None:
    command_runner(["nmcli", "device", "wifi", "connect", name])

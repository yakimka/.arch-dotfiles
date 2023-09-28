from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
import operator

from wmtools.core.command import CommandRunner, run_command
from wmtools.nmcli.tools import nmcli_output_reader


class ConnectionType(Enum):
    # ETHERNET = "802-3-ethernet"
    WIFI = "802-11-wireless"


@dataclass
class Connection:
    name: str
    autoconnect: bool
    autoconnect_priority: int
    active: bool
    type: ConnectionType



def get_saved_connections(command_runner: CommandRunner = run_command) -> List[Connection]:
    fields = "name,autoconnect,autoconnect-priority,active,type"
    result = command_runner([
        "nmcli", 
        f"--fields={fields}", 
        "--terse",
        "c",
        "show",
    ])
    connections = []
    for item in nmcli_output_reader(result.stdout, fields):
        try:
            conn_type = ConnectionType(item["type"])
        except ValueError:
            continue
        connections.append(Connection(
            name=item["name"],
            autoconnect=item["autoconnect"] == "yes",
            autoconnect_priority=int(item["autoconnect-priority"]),
            active=item["active"] == "yes",
            type=conn_type,
        ))
    connections.sort(key=operator.attrgetter("autoconnect_priority"), reverse=True)
    return connections


def connect(name: str, password: Optional[str], command_runner: CommandRunner = run_command) -> bool:
    cmd = ["nmcli", "c", "up", name]
    if password:
        cmd.append("--ask")
    result = command_runner(cmd, input=password or None)
    return result.returncode == 0


def disconnect(name: str, command_runner: CommandRunner = run_command) -> None:
    command_runner(["nmcli", "c", "down", name])


def get_property(name: str, prop: str, command_runner: CommandRunner = run_command) -> Optional[str]:
    result = command_runner(["nmcli", "-g", prop, "connection", "show", name])
    if result.returncode != 0:
        return None
    return result.stdout

def set_property(name: str, prop: str, value: str, command_runner: CommandRunner = run_command) -> None:
    command_runner(["nmcli", "connection", "modify", "id", name, prop, value])

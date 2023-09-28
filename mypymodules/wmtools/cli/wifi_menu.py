from dataclasses import dataclass
from typing import Optional, List, Callable
from functools import partial

from wmtools.core.command import CommandRunner, run_command
from wmtools.core.secret import read_password, ask_password, save_password
from wmtools.commands import WofiCommand
from wmtools.nmcli.wifi import WifiConn
from wmtools.nmcli import connections, wifi


wifi_menu_command = WofiCommand(
        dmenu=True,
        width=370,
        lines=20,
        location=3,
        xoffset=-46,
        yoffset=10,
        cache_file="/dev/null",
        allow_markup=True,
        prompt="Select network",
        # reset configuration to default
        conf="",
    )


_ACTIVE_SIGN = "\uf00c"
_SECURITY_SIGN = "\uf084"

@dataclass
class NetworkMenuItem:
    icon: str
    name: str
    active: str
    security: str

    @classmethod
    def from_network(cls, network: WifiConn):
        return cls(
            icon=network.bar,
            name=network.ssid,
            active=_ACTIVE_SIGN if network.active else " ",
            security=_SECURITY_SIGN if network.security else " ",
        )
    
    def render(self) -> str:
        return f"<tt>{self.icon:5}{self.name:34}{self.active} {self.security}</tt>"
    
    @classmethod
    def from_rendered(cls, line: str) -> Optional["NetworkMenuItem"]:
        if "<tt>" not in line or len(line) < 40:
            return None
        line = line.replace("<tt>", "").replace("</tt>", "")
        return NetworkMenuItem(
            icon=line[0:5].strip(),
            name=line[5:-3].strip(),
            active=line[-3],
            security=line[-1],
        )
    
    def to_network(self) -> WifiConn:
        return WifiConn(
            ssid=self.name,
            bar=self.icon,
            active=_ACTIVE_SIGN in self.active,
            security=_SECURITY_SIGN in self.security,
        )


class NetworkMenuManager:
    def __init__(self, networks: List[WifiConn]):
        self.networks = networks
    
    def items(self) -> List[NetworkMenuItem]:
        return [NetworkMenuItem.from_network(n) for n in self.networks]
    
    def render(self) -> str:
        return "\n".join([item.render() for item in self.items()])
    
    def parse_selected(self, line: str) -> Optional[WifiConn]:
        menu_item = NetworkMenuItem.from_rendered(line)
        if menu_item is None:
            return None
        return menu_item.to_network()


def select_network(network_menu_manager: NetworkMenuManager, command_runner: CommandRunner = run_command) -> Optional[WifiConn]:
    wifi_line, *_ = command_runner(wifi_menu_command, input=network_menu_manager.render())
    return network_menu_manager.parse_selected(wifi_line)


def main():
    networks = wifi.scan()
    selected_network = select_network(NetworkMenuManager(networks))
    if selected_network is None:
        return
    
    saved_connections = connections.get_saved_connections()
    is_new = all(c.name!= selected_network.ssid for c in saved_connections)
    
    if selected_network.active:
        connections.disconnect(selected_network.ssid)
        return
    
    wifi.connect(selected_network.ssid)
    if selected_network.security and is_new:
        connections.set_property(selected_network.ssid, "802-11-wireless-security.psk-flags", "1")


if __name__ == '__main__':
    main()

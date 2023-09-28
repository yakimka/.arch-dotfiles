import subprocess
from enum import Enum
from typing import Union, List, Tuple, NamedTuple, Callable, Protocol
from dataclasses import fields


def build_params(values: Tuple[str, str]) -> List[str]:
    params = []
    for name, value in values:
        if value is None:
            continue
        if isinstance(value, bool):
            if value:
                params.append(f'{name}')
        elif isinstance(value, Enum):
            params.append(f'{name}={value.value}')
        else:
            params.append(f'{name}={value}')
    return params


class ProcessResult(NamedTuple):
    stdout: str
    stderr: str
    returncode: int


class Command(Protocol):
    def build(self) -> List[str]:
        ...


CommandRunner = Callable[[Union[List[str], Command], Union[str, bytes, None]], ProcessResult]


def run_command(cmd: Union[List[str], Command], input: Union[str, bytes, None] = None) -> ProcessResult:
    if isinstance(input, str):
        input = input.encode('utf-8')
    if hasattr(cmd, 'build'):
        cmd = cmd.build()
    res = subprocess.run(cmd, capture_output=True, input=input)
    return ProcessResult(
        res.stdout.decode('utf-8').strip(),
        res.stderr.decode('utf-8').strip(),
        res.returncode
    )


class CommandMixin:
    BASE_ARGS = ()

    def build(self) -> List[str]:
        values = []
        for field in fields(self):
            value = getattr(self, field.name)
            field_name = f'--{field.name.replace("_", "-")}'
            values.append((field_name, value))
        return [*self.BASE_ARGS, *build_params(values)]

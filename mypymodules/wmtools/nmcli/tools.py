from typing import Dict, Generator


def nmcli_output_reader(output: str, fields: str) -> Generator[Dict[str, str], None, None]:
    fields = [f.strip() for f in fields.split(',')]
    for line in output.splitlines():
        values = line.strip().split(':')
        yield dict(zip(fields, values))

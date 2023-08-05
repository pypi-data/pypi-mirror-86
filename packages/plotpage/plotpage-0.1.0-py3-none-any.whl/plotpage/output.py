
import sys
import io
import struct
from typing import Dict, TextIO


def capture_output() -> None:
    sys.stdout = _PassThroughStringIO(sys.stdout)
    sys.stderr = _PassThroughStringIO(sys.stderr)

def get_captured_outputs() -> Dict[str, str]:
    captured_outputs = {}
    for output_name in "stdout", "stderr":
        fileobj = getattr(sys, output_name)
        if isinstance(fileobj, _PassThroughStringIO):
            captured_output = fileobj.getvalue()
            if len(captured_output):
                captured_outputs[output_name] = captured_output
    
    return captured_outputs

class _PassThroughStringIO(io.StringIO):

    def __init__(self, target: TextIO) -> None:
        super().__init__()
        self._target = target

    def write(self, s: str) -> int:
        self._target.write(s)
        return super().write(s)

def _int_to_bytes(value: int) -> bytes:
    return struct.pack(">q", value)

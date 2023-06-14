"""这就是一个测试."""
from pathlib import Path

path=Path(__file__)
if path.exists():
    dir_path = path.absolute().parent
    __path__.append(str(dir_path.joinpath("a")))
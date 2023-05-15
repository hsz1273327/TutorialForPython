# 一般用setuptools
from setuptools import setup, Command
import os
import subprocess
from typing import List, Tuple, Optional


class CoverageCommand(Command):
    description = "覆盖率"
    user_options = [
        ("output=", "o", "选择报告的输出方式")
    ]

    def initialize_options(self) -> None:
        self.cwd: Optional[str] = None
        self.output = ''

    def finalize_options(self) -> None:
        self.cwd = os.getcwd()
        if self.output and self.output not in ("report", "html"):
            raise Exception("Parameter --output is missing")

    def run(self) -> None:
        assert os.getcwd() == self.cwd, 'Must be in package root: {self.cwd}'.format(self=self)
        command = ['/usr/bin/env', 'python', '-m', 'coverage']
        if self.output:
            command.append('{self.output}'.format(self=self))
        else:
            command.append('report')
        self.announce('Running command: {command}'.format(command=str(command)),
                      level=2)
        subprocess.check_call(command)


class TestCommand(Command):
    description = "测试"
    user_options: List[Tuple[str, str, str]] = []

    def initialize_options(self) -> None:
        self.cwd: Optional[str] = None

    def finalize_options(self) -> None:
        self.cwd = os.getcwd()

    def run(self) -> None:
        assert os.getcwd() == self.cwd, 'Must be in package root: {self.cwd}'.format(self=self)
        command = ['/usr/bin/env', 'python', '-m',
                   'coverage', 'run', '--source=seg',
                   '-m', 'unittest', 'discover', '-v', '-s', 'test']
        self.announce('Running command: {command}'.format(command=str(command)),
                      level=2)
        subprocess.check_call(command)


setup(
    cmdclass={
        'coverage': CoverageCommand,
        'test': TestCommand
    }
)

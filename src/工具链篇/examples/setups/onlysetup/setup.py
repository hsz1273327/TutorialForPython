# 一般用setuptools
from setuptools import setup, find_packages, Command
# 维持不同平台文件相同的编码
from codecs import open
from os import path
import os
import subprocess
from typing import List, Tuple, Optional
import seg.version as version
here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as f:
    long_description = f.read()

# 用同文件夹下的requirements.txt文件定义运行依赖
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    REQUIREMETS = f.readlines()


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
    name='seg',
    version=version.__version__,
    url='https://github.com/xxxx/sampleproject',
    author='The Python Packaging Authority',
    author_email='pypa-dev@googlegroups.com',
    keywords=["seg", "chinese nlp"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    description='A sample Python project for seg chinese txt',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['contrib', 'docs', 'test']),
    zip_safe=False,
    license='MIT License',
    platforms=["any"],
    python_requires="~=3.10",
    install_requires=REQUIREMETS,
    extras_require={
        'gui': ['PySimpleGUI>=4.60.4'],
        'test': ['coverage'],
        'all': ['PySimpleGUI>=4.60.4', 'coverage']
    },
    entry_points={
        'console_scripts': [
            'seg = seg.cmd:cmdseg',
        ],
        'gui_scripts': [
            'seg-gui = seg.gui:guiseg',
        ]
    },
    cmdclass={
        'coverage': CoverageCommand,
        'test': TestCommand
    }
)

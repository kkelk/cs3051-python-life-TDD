from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', 'Arguments to pass to tox')]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    name = 'life',
    version = '0.0.1',
    author = '140004021',
    description = 'A simple version of Conway\'s Game of Life.',
    packages = ['life'],
    tests_require=['tox'],
    cmdclass = {'test': Tox},
)

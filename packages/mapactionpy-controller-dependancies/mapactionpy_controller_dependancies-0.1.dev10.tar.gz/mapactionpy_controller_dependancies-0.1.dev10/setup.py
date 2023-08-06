import subprocess
import sys
from setuptools import setup, find_packages
# from setuptools import find_packages
# from distutils.cmd import Command
# from distutils.command.install import install as Command
from setuptools.command.develop import develop
from setuptools.command.install import install
# from distutils.core import setup
from os import path, environ
import sys
import subprocess
from get_wheel_list import get_wheel_paths, root_dir

_base_version = '0.1'


def install_from_wheels(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.

    It modifies the run() method so that it prints a friendly greeting.

    https://blog.niteo.co/setuptools-run-custom-code-in-setup-py/
    """
    orig_run = command_subclass.run

    def modified_run(self):
        print('Custom run() method')

        if sys.platform == 'win32':
            for wheel_path in get_wheel_paths():
                # wheel_path = path.join(root_dir, 'dependency_wheels', dir_name, wheel_name)
                print('Installing {} from wheel file.'.format(wheel_path))
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', wheel_path])
                    # pip_result = pip.main(['install', wheel_path])
                    # print('pip result = {}'.format(pip_result))
                except SystemExit:
                    pass

        print('About to call default install run() method')
        orig_run(self)

    command_subclass.run = modified_run
    return command_subclass


@install_from_wheels
class CustomDevelopCommand(develop):
    pass


@install_from_wheels
class CustomInstallCommand(install):
    pass


def readme():
    with open(path.join(root_dir, 'README.md')) as f:
        return f.read()


# See https://packaging.python.org/guides/single-sourcing-package-version/
# This uses method 4 on this list combined with other methods.
def _get_version_number():
    travis_build = environ.get('TRAVIS_BUILD_NUMBER')
    travis_tag = environ.get('TRAVIS_TAG')

    if travis_build:
        if travis_tag:
            version = travis_tag
        else:
            version = '{}.dev{}'.format(_base_version, travis_build)

        with open(path.join(root_dir, 'VERSION'), 'w') as version_file:
            version_file.write(version.strip())
    else:
        try:
            ver = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
            version = '{}+local.{}'.format(_base_version, ver.decode('ascii').strip())
        except Exception:
            with open(path.join(root_dir, 'VERSION')) as version_file:
                version = version_file.read().strip()

    return version


setup(
    name='mapactionpy_controller_dependancies',
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
    },
    version=_get_version_number(),
    description='Controls the workflow of map and infographic production',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='http://github.com/mapaction/mapactionpy_controller_dependancies',
    author='MapAction',
    author_email='github@mapaction.com',
    license='GPL3',
    packages=find_packages(),
    include_package_data=True,
    test_suite='unittest',
    tests_require=['unittest'],
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Win32 (MS Windows)",
        "Operating System :: Microsoft :: Windows"
    ])

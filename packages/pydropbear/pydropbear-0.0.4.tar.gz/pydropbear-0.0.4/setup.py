"""
sdist - copy all dropbear files (defined in MANIFEST.in) and compile on setup
bdist_wheel - distributed with precompiled dropbear

Usage:
python setup.py sdist bdist_wheel
twine upload -r testpypi dist/*
twine upload dist/*
"""
import os
from distutils.command.build import build
from distutils.command.install import install
from subprocess import check_call

from setuptools import setup

BASEPATH = os.path.dirname(os.path.abspath(__file__))
DROPBEAR_PATH = os.path.join(BASEPATH, "dropbear")


class DropbearBuild(build):
    def initialize_options(self):
        super().initialize_options()

        # remove *.o files before the copy (defined in MANIFEST.in)
        check_call(["make", "clean"], cwd=DROPBEAR_PATH)

    def run(self):
        build.run(self)

        def compile_dropbear():
            check_call("autoconf", cwd=DROPBEAR_PATH)
            check_call("autoheader", cwd=DROPBEAR_PATH)
            check_call("./configure", cwd=DROPBEAR_PATH)
            check_call(
                'make PROGRAMS="dropbear dbclient dropbearkey" MULTI=1',
                cwd=DROPBEAR_PATH,
                shell=True,
            )

        self.execute(compile_dropbear, [], "Building Dropbear")
        self.mkpath(self.build_lib)

        if not self.dry_run:
            bin_path = os.path.join(DROPBEAR_PATH, "dropbearmulti")
            self.copy_file(bin_path, self.build_lib + "/pydropbear")


class DropbearInstall(install):
    def run(self):
        self.copy_tree(self.build_lib, self.install_lib)
        install.run(self)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pydropbear",
    version="0.0.4",
    author="u1234x1234",
    author_email="u1234x1234@gmail.com",
    description=("pydropbear"),
    license="MIT",
    keywords="",
    url="https://github.com/u1234x1234/pydropbear",
    packages=["pydropbear"],
    zip_safe=False,
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    cmdclass={
        "build": DropbearBuild,
        "install": DropbearInstall,
    },
)

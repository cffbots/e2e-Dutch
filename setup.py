import setuptools
import setuptools.command.build_py
import os
import tensorflow as tf
import subprocess
import pkg_resources

__version__ = None

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(os.path.join(os.path.dirname(__file__), 'e2edutch/__version__.py')) as versionpy:
    exec(versionpy.read())


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Build the tensorflow kernels, and proceed with default build."""

    def run(self):
        args = ["g++", "-std=c++11", "-shared", "-fPIC", "-O2",
                "-D_GLIBCXX_USE_CXX11_ABI=0"]
        args += ["-Wl,-rpath=" + tf.sysconfig.get_lib()]
        args += tf.sysconfig.get_compile_flags() + tf.sysconfig.get_link_flags()
        args += [
                pkg_resources.resource_filename("e2edutch", "coref_kernels.cc"),
                "-o",
                pkg_resources.resource_filename("e2edutch", "coref_kernels.so")
                ]
        subprocess.check_call(args)
        setuptools.command.build_py.build_py.run(self)


setuptools.setup(
    name="e2e-Dutch",
    version=__version__,
    author="Dafne van Kuppevelt",
    author_email="d.vankuppevelt@esciencecenter.nl",
    description="Coreference resolution with e2e for Dutch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Filter-Bubble/e2e-Dutch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={'e2edutch': ["cfg/*.conf", "coref_kernels.so"]},
    cmdclass={
        "build_py": BuildPyCommand
    },
    test_suite='test',
    python_requires='>=3.6',
    install_requires=[
        "tensorflow>=2.0.0",
        "h5py",
        "nltk",
        "pyhocon",
        "scipy",
        "scikit-learn",
        "torch",
        "transformers"
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pycodestyle',
    ],
)

from setuptools import setup, Extension
import os

pi0core_lib = os.environ.get('PI0CORE_PATH', './pi0core.so')

setup(
    name='pi0quantum',
    version='0.1.0',
    packages=['pi0quantum_pkg'],
    package_dir={'pi0quantum_pkg': 'pi0quantum_pkg'},
    include_package_data=True,
    description='Pi0System Python bindings and core operators',
    author='Pi0System Team',
    ext_modules=[
        Extension(
            'pi0quantum_pkg.pi0core',
            sources=[],
            libraries=[pi0core_lib],
            library_dirs=['.'],
        ),
    ],
    zip_safe=False,
)

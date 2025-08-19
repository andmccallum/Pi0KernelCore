
from setuptools import setup, find_packages

setup(
    name='Pi0KernelCore',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Pi0 Quantum and Mathematical Engine Core',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/Pi0KernelCore',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.19.2',
        'qutip>=4.6.0',
        'qutip-qip>=0.2.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=22.0',
            'flake8>=3.9',
            'mypy>=0.910',
        ],
    }
)

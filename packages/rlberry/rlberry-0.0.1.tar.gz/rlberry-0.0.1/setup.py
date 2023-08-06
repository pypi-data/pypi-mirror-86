from setuptools import setup, find_packages

packages = find_packages(exclude=['docs', 'notebooks', 'logo'])

install_requires = [
    'numpy>=1.17',
    'pygame',
    'joblib',
    'matplotlib',
    'seaborn',
    'pandas'
]

tests_require = [
    'pytest',
    'pytest-cov',
    'numpy>=1.17',
    'numba',
    'joblib',
    'matplotlib',
    'pandas',
    'seaborn',
    'optuna',
    'pyvirtualdisplay',
]

full_requires = [
    'numba',
    'torch>=1.6.0',
    'optuna',
    'ffmpeg-python',
    'PyOpenGL',
    'PyOpenGL_accelerate',
    'pyvirtualdisplay',
]

extras_require = {
    'full': full_requires,
    'test': tests_require,
    'deploy': ['sphinx', 'sphinx_rtd_theme'],
    'opengl_rendering': ['PyOpenGL', 'PyOpenGL_accelerate'],
    'torch_agents': ['torch>=1.6.0'],
    'hyperparam_optimization': ['optuna'],
    'save_video': ['ffmpeg-python'],
}

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='rlberry',
    version='0.0.1',
    description='An easy-to-use reinforcement learning library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='rlberry team',
    url='https://github.com/rlberry-py',
    license='MIT',
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    zip_safe=False,
)


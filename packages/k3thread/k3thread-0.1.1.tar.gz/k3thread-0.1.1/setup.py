# DO NOT EDIT!!! built with `python _building/build_setup.py`
import setuptools
setuptools.setup(
    name="k3thread",
    packages=["k3thread"],
    version="0.1.1",
    license='MIT',
    description='utility to create thread.',
    long_description='# k3thread\n\n[![Build Status](https://travis-ci.com/pykit3/k3thread.svg?branch=master)](https://travis-ci.com/pykit3/k3thread)\n![Python package](https://github.com/pykit3/k3thread/workflows/Python%20package/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/k3thread/badge/?version=stable)](https://k3thread.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3thread)](https://pypi.org/project/k3thread)\n\nutility to create thread.\n\nk3thread is a component of [pykit3] project: a python3 toolkit set.\n\n\nk3thread is utility to create and operate thread.\n\nStart a daemon thread after 0.2 seconds::\n\n    >>> th = daemon(lambda :1, after=0.2)\n\nStop a thread by sending a exception::\n\n    import time\n\n    def busy():\n        while True:\n            time.sleep(0.1)\n\n    t = daemon(busy)\n    send_exception(t, SystemExit)\n\n\n\n\n# Install\n\n```\npip install k3thread\n```\n\n# Synopsis\n\n```python\n>>> th = daemon(lambda :1, after=0.2)\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3',
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3thread',
    keywords=['thread'],
    python_requires='>=3.0',

    install_requires=['semantic_version~=2.8.5', 'jinja2~=2.11.2', 'PyYAML~=5.3.1', 'sphinx~=3.3.1', 'k3ut~=0.1.7'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)

import re
from setuptools import setup, find_packages

packages = find_packages(exclude=["tests"])
requires = ["django == 1.9"]

__version__ = ""
with open("trackmaven_django/__init__.py", "r") as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

if not __version__:
    raise RuntimeError("Cannot find version information")


def data_for(filename):
    with open(filename) as fd:
        content = fd.read()
    return content


setup(
    name="trackmaven-django",
    version=__version__,
    author="TrackMaven Engineering",
    author_email="engineering@trackmaven.com",
    url="https://github.com/trackmaven/trackmaven-django",
    packages=packages,
    include_package_data=True,
    install_requires=requires,
)

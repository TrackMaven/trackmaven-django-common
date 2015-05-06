from setuptools import setup, find_packages


setup(
    name='trackmaven-django-common',
    author="TrackMaven Engineering",
    author_email="engineering@trackmaven.com",
    version='0.0.1',
    description="",
    url="https://github.com/TrackMaven/trackmaven-django-common",
    license="MIT",
    packages=find_packages(exclude=['tests']),
)

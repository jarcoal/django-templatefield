from setuptools import setup

setup(
    name="django-templatefield",
    version="0.0.1",
    description="Django model field for saving/retrieving templates for rendering.",
    long_description=open("README.md").read(),
    keywords="django, templates",
    author="Jared Morse",
    author_email="jarcoal@gmail.com",
    url="https://github.com/jarcoal/django-templatefield",
    license="MIT",
    packages=["templatefield"],
    install_requires=['django'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
)
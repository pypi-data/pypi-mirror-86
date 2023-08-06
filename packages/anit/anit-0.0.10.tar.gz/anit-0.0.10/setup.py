
import setuptools
import anit

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anit",
    version=anit.VERSION,
    author="Animite Software Foundation",
    author_email="shaurya.p.singh21@gmail.com",
    description="May the force be with you.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    scripts=['bin/anit'],
    install_requires=[
        'yagmail',
        'pyfiglet',
        'click'
    ]
)

import setuptools

# write README.md in GitHub Flavored Markdown language:
# https://gist.github.com/stevenyap/7038119
# https://jbt.github.io/markdown-editor/
# https://github.github.com/gfm/
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyteetime",
    version="1.0.0",
    author="Rolf Sander",
    author_email="mail@rolf-sander.net",
    description="Unix tee command for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.rolf-sander.net/software/pyteetime",
    packages=setuptools.find_packages(),
    scripts=['pyteetime/tee-test.py'],
    classifiers=[ # https://pypi.org/classifiers
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: Unix",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: System :: Logging",
    ],
    python_requires='>=3.6',
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bypaxpan',
    version=0.01,
    author="Julio Lira",
    author_email="jul10l1r4@disroot.org",
    description="Ferramenta para bypassar análises de processamento de linguagem natural :knife:",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jul10l1r4/bypaxpan",
    packages=["bypaxpan"],
    license="GPLv3",
    keywords="Bypass NLP spacy ptBr",
    install_requires=[
          'spacy',
          'pysinonimos',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        ],
    )

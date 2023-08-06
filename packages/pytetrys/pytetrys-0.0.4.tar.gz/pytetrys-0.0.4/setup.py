import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytetrys",
    version="0.0.4",
    author="Equipe PyTetrys",
    author_email="adnan.bezerra@ccc.ufcg.edu.br",
    description="Versão 0.4 do futuro jogo PyTetrys",
    url="https://github.com/LucasBSousa04/PyTetris",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

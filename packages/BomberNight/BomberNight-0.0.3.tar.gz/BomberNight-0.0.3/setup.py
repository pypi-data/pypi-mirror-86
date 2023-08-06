from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='BomberNight',
    version="0.0.3",
    description='Releitura do Bomberman',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/juliohsu/BomberNight',
    author='Júlio Hsu',
    author_email='tst700900@gmail.com',
    license='MIT',
    keywords=[
        'jogo',
        'game',
        'bomberman',
        'arcade',
        'ação'
    ],
    packages=find_packages(),
    install_requires=['pygame>=2.0'],
    entry_points={
        'console_scripts': [
            'bombernight=BomberNight.__main__:main'
        ]
    },
    python_requires='>=3.6',
    include_package_data=True,
)
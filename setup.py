from setuptools import setup, find_packages

setup(
    name='MineNBT',
    version='0.1.0',
    packages=find_packages(),
    description='MineNBT is a lightweight, efficient Python library designed to read and write Minecraft\'s Named Binary Tag (NBT) data. ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Theoreb',
    author_email='espagnol.dali@gmail.com',
    url='https://github.com/Theoreb/MineNBT',
    install_requires=[
        # Any dependencies, e.g., 'requests >= 2.23.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

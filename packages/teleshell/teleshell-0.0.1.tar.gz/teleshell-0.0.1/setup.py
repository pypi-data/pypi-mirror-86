from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='teleshell',
    version='0.0.1',
    description='A shell for telethon',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://notabug.org/EgTer/teleshell',
    author='EgTer',
    author_email='annom2017@mail.ru',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='telethon, shell',
    package_dir={'': 'teleshell'},
    packages=find_packages(where='teleshell'),
    python_requires='>=3.5, <4',
    install_requires=['telethon'],
    project_urls={
        'Source': 'https://notabug.org/EgTer/teleshell',
    },
)

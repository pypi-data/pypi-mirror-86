from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(
    name='simplelayout-aoweiie',
    version='1.0.0',
    description='a simple layout generator project',
    long_description=long_description,  # Optional
    url='https://github.com/idrl-assignment/3-simplelayout-package-aoweiie',
    author='Yao WJ',
    author_email='996267113@qq.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='layout',

    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['numpy', 'matplotlib', 'scipy'],
    entry_points={
        'console_scripts': [
                'simplelayout=simplelayout.__main__:main',
            ],
        },
    project_urls={
        'Source': 'https://github.com/idrl-assignment/3-simplelayout-package-aoweiie',
        }
    )

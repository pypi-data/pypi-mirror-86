from setuptools import setup, find_packages
setup_args = dict(
    name='ofekWOG',
    version='0.1.1',
    description='Play with Fun',
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    author='ofek krispel',
    keywords=['games', 'ofekkrispel', 'ofekgame'],
    download_url='https://pypi.org/project/elastictools/'
)

include_package_data=True

if __name__ == '__main__':
    setup(**setup_args)
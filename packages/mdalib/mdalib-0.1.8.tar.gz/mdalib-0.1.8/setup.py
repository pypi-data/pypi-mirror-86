from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='mdalib',
    version='0.1.8',
    description='ทดสอบ',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Krit Naja',
    # author_email='gthuc.nguyen@gmail.com',
    keywords=['MDA', 'kafka'],
    # url='https://github.com/ncthuc/mdalib',
    download_url='https://pypi.org/project/mdalib/'
)

# install_requires = [
#     'kafka-python==2.0.2',
#     'msgpack==1.0.6',
#     'requests==2.22.0'
# ]


install_requires = [
    'kafka-python',
    'msgpack',
    'requests'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
from io import open

from setuptools import setup

# python setup.py sdist --formats=zip
# python setup.py sdist bdist_wheel
# twine upload dist/halo_aws-0.11.41.tar.gz -r pypitest

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='halo-aws',
    version='0.12.1',
    packages=['halo_aws', 'halo_aws.providers', 'halo_aws.providers.cloud', 'halo_aws.providers.cloud.aws'],
    url='https://github.com/yoramk2/halo_aws',
    license='MIT License',
    author='yoramk2',
    author_email='yoramk2@yahoo.com',
    description='this is the Halo framework library for aws',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)

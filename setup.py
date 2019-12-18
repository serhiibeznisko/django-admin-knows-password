import os
from setuptools import setup, find_packages


def get_package_data(package):
    start = len(package) + 1  # strip package name
    for path, dirs, files in os.walk(package):
        for file in files:
            if file.startswith('.') or file.endswith('.py') or file.endswith('.pyc'):
                continue
            yield os.path.join(path[start:], file)


setup(
    name='django_admin_knows_password',
    packages=find_packages(),
    package_data={
        'django_admin_knows_password': list(get_package_data('django_admin_knows_password')),
    },
    version='0.5',
    license='MIT',
    description='Django package that provides widget to display images.',
    author='Serhii Beznisko',
    author_email='beznisko.ss@gmail.com',
    url='https://github.com/serhiibeznisko/django-admin-knows-password',
    keywords=['django', 'admin', 'user', 'password', 'widget'],
    install_requires=[
        'django',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

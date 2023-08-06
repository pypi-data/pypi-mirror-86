from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup_requires = [
    'setuptools_scm'
]

install_requires = [
    'django~=2.2',
    'djangorestframework~=3.11',
    'django-filter~=2.3'
]

setup(
    name='django-budget-backend',
    description='An API to manage your monthly budgets.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/personal-server/django-budget-backend',
    author='Sheldon Woodward',
    author_email='me@sheldonw.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 2.2',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='django budget backend',
    packages=['budget'],
    python_requires='~=3.8',
    setup_requires=setup_requires,
    install_requires=install_requires,
    use_scm_version=True
)

import setuptools

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    # Use VCS instead of MANIFEST to control included files & folders
    # Works for git and hg
    use_scm_version=False,
    setup_requires=['setuptools_scm'],
    include_package_data=True,  # Needed if using old MANIFEST.in?

    # Mandatory fields
    name='fun-supergus',
    version='0.1.3',
    packages=setuptools.find_packages(),    # Builds & wheels are limited to pkgs specified here

    # Optional fields
    # scripts=['bin/'],    # Rely on VCS?
    license='LICENSE',
    author='Christopher Couch',
    author_email='christopher.couch@gmail.com',
    description='Toolkit for various fun and useful tasks',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/supergus/fun',

    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
    ],

    keywords='fun utilities email SMS',

    python_requires='>=3.7',

    project_urls={
        'Source': 'https://github.com/supergus/fun',
    },
)

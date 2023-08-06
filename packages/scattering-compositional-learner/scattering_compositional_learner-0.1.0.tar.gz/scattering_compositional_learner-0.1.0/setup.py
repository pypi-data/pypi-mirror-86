from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='scattering_compositional_learner',
    version='0.1.0',
    author='Mikołaj Małkiński',
    author_email='mikolaj.malkinski@gmail.com',
    license='MIT',
    description="Scattering Compositional Learner for solving Raven's Progressive Matrices",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mikomel/scattering-compositional-learner',
    keywords=['artificial intelligence', 'scattering compositional learner'],
    install_requires=[
        'torch>=1.5'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)

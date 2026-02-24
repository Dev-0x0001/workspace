from setuptools import setup, find_packages

setup(
    name='performance-monitor',
    version='0.1.0',
    author='Performance Team',
    author_email='performance@example.com',
    description='Performance monitoring and baseline comparison tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your-org/performance-monitor',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'perf-compare=performance_monitor.cli:main',
        ],
    },
)
try:
    # pip >=20
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    try:
        # 10.0.0 <= pip <= 19.3.1
        from pip._internal.download import PipSession
        from pip._internal.req import parse_requirements
    except ImportError:
        # pip <= 9.0.3
        from pip.download import PipSession
        from pip.req import parse_requirements
import setuptools

install_reqs = parse_requirements('requirements.txt', session=False)
try:
    requirements = [str(ir.req) for ir in install_reqs]
except:
    requirements = [str(ir.requirement) for ir in install_reqs]

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="eslite-movie",
    version="1.0.1",
    author="Cliff Lin",
    author_email="zylintw@gmail.com",
    description="eslite movie crawler",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/CliffLin/eslite-movie",
    packages=['eslite_movie'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    entry_points={
        'console_scripts': ['eslite-movie=eslite_movie.cli:main']
    },
    python_requires='>=3.6',
)

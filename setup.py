from setuptools import setup
import pathlib

from version.progsettings import get_version

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

version = get_version()

setup(
    name="progscheduler",
    version=version,
    description="A simple automated task to schedule files to open in specific days of the week or every day at startup or at specific time of the "
                "day.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zaytiri/program-scheduler",
    project_urls={
        'GitHub': 'https://github.com/zaytiri/program-scheduler',
        'Changelog': 'https://github.com/zaytiri/program-scheduler/blob/main/CHANGELOG.md',
    },
    author="zaytiri",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    keywords="program, schedule, scheduler, startup, days, open, files, folders",
    package_data={'progscheduler': ['progsettings.yaml']},
    packages=["progscheduler", "progscheduler.settings", "progscheduler.utils"],
    python_requires=">=3.10.6",
    install_requires=[
      "PyYAML~=6.0",
      "schedule~=1.1.0"
    ],
    entry_points={
        "console_scripts": [
            "progscheduler=progscheduler:app.main",
        ],
    }
)
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Status
- Added
- Changed
- Fixed
- Removed

## [2.0.0] - 2023-03-22

### Changed
- auto management of program arguments and settings were refactored. now uses the following library ['margument'](https://pypi.org/project/margument/) for that purpose.
- changed some arguments commands, for example: use '-p' to specify file path instead of '-e'.

### Added
- added new argument option to exit program terminal/cmd window when all scheduled jobs are done.
- added new argument option to define the time for the scheduler to no longer run, for example: if time defined is '17:00', the scheduler, if started, will no longer run if current time exceeds defined time.
- added new argument option to also list all global configs. previously, only scheduled jobs were being listed.
- added new argument option specific for running the progscheduler. now the program will only start doing its scheduled jobs if this argument is specified. if not, the program can list settings, update schedules, create new ones, do nothing etc., all without running automatically after every configuration.
- added more user-friendly messages.

### Fixed
- updated README.md file.

## [1.0.1] - 2022-11-20

### Changed
- README.md file was updated
- added new options when choosing the days to schedule. added 'weekdays' and 'weekends' option.

## [1.0.0] - 2022-11-20

### Added
- First release on PyPI
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Status
- Added
- Changed
- Fixed
- Removed

## [2.3.1] - 2023-04-01

### Fixed
- fixed issue where old dates already configured in 'exclude' and 'include' lists in each scheduled job settings, were being considered when updating these arguments, making an error appear which would block any further updates. Now any old dates already configured will be removed when updating these settings.

## [2.3.0] - 2023-03-28

### Added
- validation for verifying if the alias is present in the arguments if there is any configurable setting for a scheduled job.
- new argument 'include' for each scheduled job which does the opposite of 'exclude' argument. It indicates a list of dates that a scheduled job should run that it wouldn't normally do. Any dates inserted will replace any previous configured dates in saved 'include' argument.
- validation for dates in 'include' and 'exclude' arguments, meaning the same date cannot be inserted in both configurations at the same time for a scheduled job.
- validation for when a scheduled job's path does not exist.

### Changed
- updated help messages from some arguments.
- updated README.md file.

## [2.2.0] - 2023-03-27

### Added
- new argument 'status' for each scheduled job. This will indicate if a specific job will be active or inactive (e.g. if it will run or not). This setting is to be used for when a scheduled job should not run for an unknown period of time. Could be changed anytime.
- new argument 'exclude' for each scheduled jobs to exclude days, meaning a job will not run in any date that is excluded in the configuration. Could be excluded more than one date, always with the following format: dd/mm/yyyy. Any inserted date will replace any dates configured before.

## [2.1.1] - 2023-03-26

### Fixed
- fixed time issue where the scheduled jobs wouldn't run if the device's time changed. if the time changed for an hour forward on the device, the scheduled jobs wouldn't run because using utcnow() gives a general date. The time should be equal to the device's time.
- fixed issue where the given path for a specific scheduled job, in the arguments, would not be checked properly if it existed or not.

## [2.1.0] - 2023-03-25

### Changed
- argument '--time-to-stop' is now a specific setting for each scheduled job instead of a global configuration. This means each scheduled program has more flexibility regarding the time to don't run, if progscheduler runs again.

### Fixed
- for each scheduled job, the program now checks if current day is the day to schedule. This will prevent the scheduler to stop scheduling a job that is not going to do that day.

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
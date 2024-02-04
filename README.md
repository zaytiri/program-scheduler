[![Downloads](https://pepy.tech/badge/progscheduler)](https://pepy.tech/project/progscheduler)

# Program Scheduler GUI + CLI

A simple way of scheduling files at startup or at specific time of the day. The file can also be scheduled to start at specific days of the week or every day. 

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [License](#license)
- [Status](#status)

<a name="description"></a>

## Description

The current project provides a simple automated task to schedule files to open in specific days of the week or every day at startup or at specific time of the day. Multiple files can be scheduled.

For the progscheduler to work as intended, the startup feature includes having to add a file containing the command for starting the progscheduler in a specific startup folder for Windows users. If that's not done, then the progscheduler continues to work fine but to have the scheduled files to open, the user must run the progscheduler manually every time. If the 'program-scheduler.bat' exists, double-click this file to start running the program. This is explained in [here](#installation).

A scheduled file can also be any type of file including folders. See [Notes](#notes).

<a name="gui"></a>

## GUI

### First time

1. When using the GUI for the first time, you need to have the CLI installed. You can do this by:
- On the GUI:
  - Go to 'Options' > Click on 'INSTALL CLI'. The CLI should be installed and any information will be displayed in the 'Run' tab.
- On the Command Propmt:
  - Follow [Instalation](#installation) section in this README file.

2. After everything's installed, you will have no configurations defined so you need to add some. You can do this by going to the 'Add' tab.

### _Run_

Here you can see what the program is doing when running the defined schedules.

If necessary, you can also manually run the shedules, in any given time, by clicking the 'RUN' button.

![1](https://github.com/zaytiri/program-scheduler/blob/main/readme-imgs/1.png)

### _Groups_

Ths feature will be comming in the future.

### _View/Edit_

Here you can view all your defined schedules and their respective configurations by selecting any entry in the left list. You can edit any configuration in this window, always taking in consideration the limits and options the program offers, displayed in the [Usage](#usage) section.

You can also delete any configuration when selected.

For more information, some input fields have tooltips that can be viewed by hovering the mouse over them.

![4](https://github.com/zaytiri/program-scheduler/blob/main/readme-imgs/4.png)

When selecting 'browser' entry:<br>
![4.1](https://github.com/zaytiri/program-scheduler/blob/main/readme-imgs/4.1.png)

### _Add_

In the following tab, you can add a new schedule by providing:
- 'alias': a unique name to identify this schedule;
- 'path': the path of the executable to be scheduled. The following sections are important to know: [Important](#important) and [Notes](#notes). You can 'Browse' through your files and/or you can also modify the input field as needed.

![2](https://github.com/zaytiri/program-scheduler/blob/main/readme-imgs/2.png)

### _Options_

You can also set multiple options such as the GUI theme. 

- 'Set exit when scheduler is done': If enabled, means that the window where the schedules are running will exit when they are all finished. This does not happen when schedules are run manually through the 'Run' tab.
- Theme: This option is not saved, meaning it will not persist through different instances.
- 'INSTALL CLI': It will install the progscheduler program through the command line in the background. This is needed because it contains all the features used by the GUI.
- 'ENABLE STARTUP OPTION': Two folders will be opened which mean that you will need to copy the file called "program-scheduler.bat" to the other opened folder. You can also either copy this executable to this "Startup" folder (to start this GUI automatically) or add this executable as a schedule.
  - This needs to be done if you want the main feature of the program, which is automatically start any file when the computer boots up.
- 'OPEN CONFIGURATIONS FOLDER': It will open the folder where all schedules configurations are saved. This file should not be modified unless you kow how to modify it.

![3](https://github.com/zaytiri/program-scheduler/blob/main/readme-imgs/3.png)

<a name="features"></a>

## Features

| Status | Features                                                               |
|:-------|:-----------------------------------------------------------------------|
| ✅      | schedule a file to start/open at specific days of the week or everyday |
| ✅      | schedule a file to start/open at specific time of the day              |
| ✅      | schedule a file to start/open when the computer boots up               |
| ✅      | configuration of multiple files to schedule                            |
| ✅      | see current configurations                                             |

Any new features are **_very_** welcomed.

### Future features

- Currently, the progscheduler only starts/opens a file, but in the future, a file can also be configured to do other types of jobs.

#### Done ✅
- ~~Currently, the progscheduler never stops running the scheduler, but it can be implemented that if all scheduled jobs are at startup, and they already finished then the progscheduler could stop automatically until manually started or computer rebooted.~~

Any unimplemented features will be developed by user request, so if you want any of these or new ones, open an issue.

<a name="prerequisites"></a>

## Prerequisites

[Python 3](https://www.python.org/downloads/) must be installed.

Must be used the latest version of [margument](https://pypi.org/project/margument/) library.

<a name="installation"></a>

## Installation

```
pip --no-cache-dir install progscheduler
```

or,

```
pip3 --no-cache-dir install progscheduler
```

### Windows users
To enable the startup feature, the file 'program-scheduler.bat' is provided. This file can be found in this [project's github repository](https://github.com/zaytiri/program-scheduler/blob/main/program-scheduler.bat). 

The 'program-scheduler.bat' needs to be put into 
```
C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup 
```
folder to start running when the computer boots up.

This will open a command prompt window automatically when the computer boots up. This window should only be closed if all desired jobs are already finished.

### Linux Users
Open an issue if you need to know how to enable this feature in Linux.

<a name="usage"></a>
## Usage

| Command (shortcut)                   | Command (full)                       | Type                                     | Description                                                                                                                                                                                           |
|:-------------------------------------|:-------------------------------------|------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --run                                | --run                                | **REQUIRED** for the scheduler to run    | if specified, the scheduler will start running using user-defined configurations.                                                                                                                     |
| -a                                   | --alias                              | **REQUIRED** to create new scheduled job | file alias. this name is UNIQUE within all scheduled files. to create or update any configuration regarding a specific file, this is required.                                                        |
| -p                                   | --path                               | **REQUIRED** to create new scheduled job | absolute path of file to schedule (including the extension name except for folders).                                                                                                                  |
| -d                                   | --days                               | **REQUIRED** to create new scheduled job | days to schedule a file within the following options: 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'everyday', 'weekdays' and 'weekends'.                            |
| -t                                   | --time                               | **OPTIONAL**                             | specific time to start/open a file. default is '' (empty). if time is empty then the file will start when the progscheduler command is run (at startup if program-scheduler.bat file was configured). |
| -ts                                  | --time-to-stop                       | **OPTIONAL**                             | define a time for a specific scheduled job to stop running if progscheduler runs.                                                                                                                     |
| -del                                 | --delete                             | **OPTIONAL**                             | delete a existing configuration with the file alias.                                                                                                                                                  |
| -ls                                  | --schedules                          | **OPTIONAL**                             | list all global settings.                                                                                                                                                                             |
| -lsch                                | --settings                           | **OPTIONAL**                             | list all scheduled jobs.                                                                                                                                                                              |
| -st                                  | --status                             | **OPTIONAL**                             | sets the status of a specific scheduled job. choices are: 'on' and 'off'. this indicates if a job will run(active-on) or not(inactive-off). default value is 'on'.                                    |
| -ex                                  | --exclude                            | **OPTIONAL**                             | any dates given will be excluded from the job, meaning a specific scheduled job will not run in any date specified in excluded days.                                                                  |
| -in                                  | --include                            | **OPTIONAL**                             | any dates given will be included in a job, meaning a specific scheduled job will run in any date specified in included days.                                                                          |
| --exit-when-done/--no-exit-when-done | --exit-when-done/--no-exit-when-done | **OPTIONAL**                             | boolean value. if specified, the program window will exit automatically when all scheduled jobs finished that particular day. default value: false                                                    |

<a name="important"></a>

### Important
1. -a command is always required when configuring.
2. -p, -d command is required only the first time to configure a file to schedule.
3. If the file is an executable file, **it's recommended to input the absolute path to a shortcut** instead of the original file location because if so, the executable file **may not start at all**. If a shortcut is used, the extension '.lnk' is needed. For instance: 'C:\Users\<!username>\Desktop\ExecutableShortcutWithEXEExtension.lnk'

<a name="notes"></a>

### Notes

- **By 'file', it means that the progscheduler can schedule executable files, text files, folders, or any type of file to start/open.**
- If a specific time is set, the file will only start/open from the moment the progscheduler starts running. Meaning if a file is scheduled to start at 08:00 and the progscheduler only starts running at 08:30, then the next time the file will start is at 08:00 the next day (if the progscheduler is running).
- If a file needs to be scheduled using mixed configurations, for instance, a folder needs to be opened at startup on monday but on 08:15 on friday, then the same file can be configured but always using different file alias.
- Any old dates included in 'exclude' and 'include' lists in configurations will be removed whenever these arguments are updated for a specific scheduled job.

---

Any additional help can be provided if the following command is run:

```
progscheduler --help
```
or,
```
progscheduler -h
```

Before running the scheduler, at least one program needs to be configured. The following command will configure the 'program.exe' to start when the computer boots up every monday, friday and saturday
```
progscheduler -a ProgramOrFolderToScheduleUniqueName -p "C:\Users\<username>\Desktop\program.exe" -d monday friday saturday
```

To configure an existing program to change time to schedule. The following command would schedule a program to start every day and at 08:00:
```
progscheduler -a ProgramOrFolderToScheduleUniqueName -t "08:00"
```

To add excluded days to 'ProgramOrFolderToScheduleUniqueName' configuration:
```
progscheduler -a ProgramOrFolderToScheduleUniqueName -ex 29/03/2023 1/5/2023
```

The following is an example of the previous configuration of the 'ProgramOrFolderToScheduleUniqueName' scheduled job:
```yaml
ProgramOrFolderToScheduleUniqueName:
  alias: ProgramOrFolderToScheduleUniqueName
  days:
  - monday
  - friday
  - saturday
  exclude: 
  - 29/03/2023
  - 1/5/2023
  include: []
  path: C:\Users\<username>\Desktop\program.exe
  status: 'on'
  time: 08:00
  time_to_stop: 'off'
```

To configure an existing program to change days to schedule:
```
progscheduler -a ProgramOrFolderToScheduleUniqueName -d everyday
```

To empty out the 'exclude' and/or include arguments, just add the desired argument without anything after it:
```
progscheduler -a ProgramOrFolderToScheduleUniqueName -ex -in
```

To configure any global configuration just use the argument to change:
```
> progscheduler --exit-when-done        # will close terminal/command prompt window automatically.
> progscheduler --no-exit-when-done     # will do nothing.
```

To delete an existing configuration:
```
progscheduler -del ProgramOrFolderToScheduleUniqueName
```

When all desired files are scheduled in the configurations, the following command will run the scheduler considering every configuration made:
```
progscheduler --run
```

Once the progscheduler starts running it will not stop alone, to cancel just run CTRL + C or close the terminal window. The exception to this is if the '--exit-when-done' is enabled.

<a name="support"></a>

## Support
 If any problems occurs, feel free to open an issue.

<a name="license"></a>

## License

[MIT](https://choosealicense.com/licenses/mit/)

<a name="status"></a>

## Status

This project was developed for both need and educational purposes, so I'm available to maintain this project, so any bugs, suggestions, new features, improvements, etc, don't hesitate to ask, open an issue or a pull request.

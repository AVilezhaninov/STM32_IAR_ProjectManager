## IAR EWARM project manager for STM32F M0, M3, M4, M7 MCU

IPM is small python 3.6 program that helps to create and manage IAR EWARM projects
for STM32F microconrollers with M0, M3, M4, M7 core (and other with same ST CMSIS structure).

Program capabilities:
  - create new project with ST CMSIS files;
  - add folder struct in existing project;
  - clean EWARM workspace folder;
  - rename existing workspace and project;

---

## Requirements

### Folder requirements

Program works with next project's folder struct:
- Project/
  - EWARM/
    - project.ewp
    - project.eww
  - source/
    - CMSIS/
    - user/
      - inc/
      - src/

Project is the root folder. EWARM folder contains IAR EWARM files such as workspace file, project file
and build files. Source folder contains user's files and other source files and folders.
In source directory only CMSIS is mandatory folder.

### Python requirements

Program were written with Python 3.6.0 and has **LXML** dependencies.

---

## Usage

For begin just download IPM program, IPM's template folder and your device's ST CMSIS folder in
the same directory, like this:
- some_folder/
  - CMSIS/
  - template/
  - ipm

and type `ipm <command> <args> [-h | --help]` with next commands:

| command | description |
|---------|-------------|
| create | Create new project |
| add_folder | Copy folder to project and add folder in project file |
| clean | Clean workspace folder |
| rename_workspace | Rename workspace |
| rename_project | Rename project |
| rename | Rename both workspace and project |

For details use: `ipm <command> -h`


###  Create new project
Create new IAR EWARM project with specified name and device.

`ipm create <name> <device> [-h | --help]`

| parameter | description |
|---------|-------------|
| -n, --name \<name> | New project name |
| -d, --device \<device> | New project device |

Device must be specified as in your "CMSIS/Device/ST/STM32Fxxx/Include/stm32fxxx.h".

After project creation you only have to fix:
- processor variant in IAR EWARM program (project options -> General options -> Processor variant) to your exact device;
- device defined symbol in IAR EWARM program (project options -> C/C++ compiler -> Preprocessor -> Defined symbols) to your exact device;

#### Example
`ipm create -n Project_name -d stm32f407xx`

will create new "Project_name" folder and project, copy all necessary files and
configure project to use STM32F407xx device.


### Add folder to project
Copy folder to project source directory and add folder in project folder stucture.

`ipm add_folder <project_path> <folder_path> [ignore] [-h | --help]`

| parameter | description |
|---------|-------------|
| -p, --project_path \<path> | Project path |
| -f, --folder_path \<path> | Folder path |
| -i, --ignore \<ignore> | Ignore file extentions |

Just specify project path, folder to add path and ignore
extentions devided with "/" char (for example "-i c/h/cpp/icf/").

#### Example
`ipm add_folder -p Project_name/EWARM/project_name.ewp -f folder_to_add -i s/icf`

will copy "folder_to_add" to project source directory and
add this folder in project folder stucture except *.s and *.icf files.


### Clean project
Clean workspace folder - delete all files and folders except *.eww and *.ewp.

`ipm clean <workspace_path> [-h | --help]`

| parameter | description |
|---------|-------------|
| -w, --workspace_path \<path> | Workspace path |

Just specify workspace path.

#### Example
`ipm clean -w Project_name/EWARM/project_name.eww`

will clean "project_name" workspace.


### Rename workspace
Rename workspace with specified name.

`ipm rename_workspace <workspace_path> <name> [-h | --help]`

| parameter | description |
|---------|-------------|
| -w, --workspace_path \<path> | Workspace path |
| -n, --name \<name> | New workspace name |

Just specify workspace path and new workspace name.

#### Example
`ipm rename_workspace -w Project_name/EWARM/project_name.eww -n New_name`

will rename "project_name" workspace to "New_name".


### Rename project
Rename project with specified name.

`ipm rename_project <project_path> <workspace_path> <name> [-h | --help]`

| parameter | description |
|---------|-------------|
| -p, --project_path \<path> | Project path |
| -w, --workspace_path \<path> | Workspace path |
| -n, --name \<name> | New project name |

Just specify project path, workspace containing this project path
and new project name.

#### Example
`ipm rename_project -p Project_name/EWARM/project_name.ewp -w Project_name/EWARM/project_name.eww -n New_name`

will rename "project_name" project to "New_name".


### Rename both workspace and project
Rename both workspace and project with specified name.

`ipm rename <project_path> <workspace_path> <name> [-h | --help]`

| parameter | description |
|---------|-------------|
| -p, --project_path \<path> | Project path |
| -w, --workspace_path \<path> | Workspace path |
| -n, --name \<name> | New project name |

Just specify project path, workspace containing this project path
and new project name.

#### Example
`ipm rename -p Project_name/EWARM/project_name.ewp -w Project_name/EWARM/project_name.eww -n New_name`

will rename both "project_name" workspace and project to "New_name"/

---

## Licence
MIT Licence

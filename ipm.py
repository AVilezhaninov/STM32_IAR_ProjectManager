#!/usr/bin/python3


# MIT License

# Copyright (c) 2017 Aleksey Vilezhaninov

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import argparse
import os
import sys
import shutil
from lxml import etree


# ------------------------------------------------------------------------------
# Help messages ----------------------------------------------------------------
# ------------------------------------------------------------------------------
MAIN_HELP_MESSAGE = '''
IPM - IAR Embedded Workbench project manager for STM32F M0, M3, M4, M7 MCU.

Program capabilities:
  - create new project with standart ST CMSIS files;
  - add folder struct in existing project;
  - clean EWARM workspace folder;
  - rename existing workspace and project;

usage: ipm <command> <args> [-h | --help]

commands:
    create              Create new project
    add_folder          Copy folder to project and add folder in project file
    clean               Clean workspace folder
    rename_workspace    Rename workspace
    rename_project      Rename project
    rename              Rename both workspace and project

For details use: ipm <command> -h

IPM v0.1  Copyright (c)  2017  Aleksey Vilezhaninov  a.vilezhaninov@gmail.com
'''

CREATE_HELP_MESSAGE = '''
Create new IAR EWARM project with specified name and device.

usage: ipm create <name> <device> [-h | --help]

parameters:
  -n, --name <name>      New project name
  -d, --device <device>  New project device

Device must be specified as in "CMSIS/Device/ST/STM32Fxxx/Include/stm32fxxx.h".
For usage - download IPM executable file, IPM "template" folder and
standart ST CMSIS folder in the same folder and run program.
'''

ADD_FOLDER_HELP_MESSAGE = '''
Copy folder to project source directory and ddd folder in project file.

usage: ipm add_folder <project_path> <folder_path> [ignore] [-h | --help]

parameters:
  -p, --project_path <path>     Project path
  -f, --folder_path <path>      Folder path
  -i, --ignore <ignore>         Ignore file extentions

For usage - just specify project path, folder to add path and ignore
extentions devided with "/" char (for example "-i c/h/cpp/icf/").
'''

CLEAN_HELP_MESSAGE = '''
Clean workspace folder - delete all files and folders except *.eww and *.ewp.

usage: ipm clean <workspace_path> [-h | --help]

parameters:
  -w, --workspace_path <path>   Workspace path

For usage - just specify workspace path.
'''

RENAME_WORKSPACE_HELP_MESSAGE = '''
Rename workspace with specified name.

usage: ipm rename_workspace <workspace_path> <name> [-h | --help]

parameters:
  -w, --workspace_path <path>   Workspace path
  -n, --name <name>             New workspace name

For usage - just specify workspace path and new workspace name.
'''

RENAME_PROJECT_HELP_MESSAGE = '''
Rename project with specified name.

usage: ipm rename_project <project_path> <workspace_path> <name> [-h | --help]

parameters:
  -p, --project_path <path>     Project path
  -w, --workspace_path <path>   Workspace path
  -n, --name <name>             New project name

For usage - just specify project path, workspace containing this project path
and new project name.
'''

RENAME_HELP_MESSAGE = '''
Rename both workspace and project with specified name.

usage: ipm rename <project_path> <workspace_path> <name> [-h | --help]

parameters:
  -p, --project_path <path>     Project path
  -w, --workspace_path <path>   Workspace path
  -n, --name <name>             New project name

For usage - just specify project path, workspace containing this project path
and new project name.
'''




# ------------------------------------------------------------------------------
# Argparser configuration
# ------------------------------------------------------------------------------
def CreateArgParser():
    # Parser config ------------------------------------------------------------
    parser = argparse.ArgumentParser(add_help = False)
    parser.add_argument("-h", "--help", action = "store_const", const = True)
    subparsers = parser.add_subparsers(dest = "command")

    # Create command -----------------------------------------------------------
    create_parser = subparsers.add_parser("create", add_help = False)
    create_parser.add_argument("-n", "--name", help = "New project name")
    create_parser.add_argument("-d", "--device", help = "New project device")
    create_parser.add_argument("-h", "--help", help = "Help",
                               action = "store_const", const = True)

    # Add folder command -------------------------------------------------------
    add_folder_parser = subparsers.add_parser("add_folder", add_help = False)
    add_folder_parser.add_argument("-p", "--project_path",
                                   help = "Project path")
    add_folder_parser.add_argument("-f", "--folder_path",
                                   help = "Folder path")
    add_folder_parser.add_argument("-i", "--ignore",
                                   help = "Ignore extentions")
    add_folder_parser.add_argument("-h", "--help", help = "Help",
                                   action = "store_const", const = True)

    # Clean command ------------------------------------------------------------
    clean_parser = subparsers.add_parser("clean", add_help = False)
    clean_parser.add_argument("-w", "--workspace_path", help = "Workspace path")
    clean_parser.add_argument("-h", "--help", help = "Help",
                              action = "store_const", const = True)

    # Rename workspace command -------------------------------------------------
    rename_workspace_parser = subparsers.add_parser("rename_workspace",
                                                    add_help = False)
    rename_workspace_parser.add_argument("-w", "--workspace_path",
                                         help = "Workspace path")
    rename_workspace_parser.add_argument("-n", "--name",
                                         help = "New workspace name")
    rename_workspace_parser.add_argument("-h", "--help", help = "Help",
                                         action = "store_const", const = True)

    # Rename project command ---------------------------------------------------
    rename_project_parser = subparsers.add_parser("rename_project",
                                                  add_help = False)
    rename_project_parser.add_argument("-p", "--project_path",
                                       help = "Project path")
    rename_project_parser.add_argument("-w", "--workspace_path",
                                       help = "Workspace path")
    rename_project_parser.add_argument("-n", "--name",
                                       help = "New project name")
    rename_project_parser.add_argument("-h", "--help", help = "Help",
                                       action = "store_const", const = True)

    # Rename command -----------------------------------------------------------
    rename_parser = subparsers.add_parser("rename", add_help = False)
    rename_parser.add_argument("-p", "--project_path",
                               help = "Project path")
    rename_parser.add_argument("-w", "--workspace_path",
                               help = "Workspace path")
    rename_parser.add_argument("-n", "--name",
                               help = "New project and workspace name")
    rename_parser.add_argument("-h", "--help", help = "Help",
                               action = "store_const", const = True)

    return parser




# ------------------------------------------------------------------------------
# Create new IAR EWARM project with specified name and device
# ------------------------------------------------------------------------------
def Create(project_name, project_device):
    if not os.path.exists(project_name):
        if project_device.lower()[0:6] == "stm32f":
            # Copy source files and folders
            CopyEWARMFiles(project_name)
            CopyCMSISFiles(project_name, project_device)
            ChangeProjectFile(project_name, project_device)

            # Create user folders
            MakeDir(project_name + "/source/user/inc")
            MakeDir(project_name + "/source/user/src")

            # Copy main.c to project source folder
            shutil.copy2("./template/template_main.c",
                         project_name + "/source/user")
            text_to_replace = '#include "stm32f4xx.h"'
            replace_text = '#include "stm32f' + project_device[6] + 'xx.h"'
            ReplaceTextInFile(project_name + "/source/user/template_main.c",
                              text_to_replace, replace_text)

            # Rename template_main.c
            rename_path = project_name + "/source/user"
            try:
                os.rename(rename_path + "/template_main.c",
                          rename_path + "/main.c")
            except OSError:
                Exit("Can not rename \"" + rename_path +
                     "/template_main.c\" file")
        else:
            Exit("Undefined device")
    else:
        Exit("\"" + project_name + "\" folder already exists")


# Copy and rename EWARM workspace and project template files
def CopyEWARMFiles(project_name):
    if os.path.exists("template"):
        # Create EWARM folder
        MakeDir(project_name + "/EWARM")

        # Copy template files
        src = "template/template.eww"
        dst = project_name + "/EWARM"
        CopyFile(src, dst)

        src = "template/template.ewp"
        dst = project_name + "/EWARM"
        CopyFile(src, dst)

        # Rename template files in EWARM folder
        project_file = project_name + "/EWARM/template.ewp"
        workspace_file = project_name + "/EWARM/template.eww"
        RenameProject(project_file, workspace_file, project_name)
        RenameWorkspace(workspace_file, project_name)

    else:
        Exit("Can not find \"template\" folder")


# Copy CMSIS files in project CMSIS folder
def CopyCMSISFiles(project_name, project_device):
    device = project_device.lower()
    device_family = project_device[0:7].upper() + "xx"

    if os.path.exists("CMSIS"):
        # Copy ./CMSIS/Include folder with all files
        src = "CMSIS/Include"
        dst = project_name + "/source/CMSIS/Include"
        CopyTree(src, dst)

        # Copy CMSIS"s files and create folders
        directory = project_name + "/source/CMSIS/Lib/ARM"
        MakeDir(directory)

        directory = project_name + "/source/CMSIS/Device/ST/"
        directory += device_family + "/Include"
        MakeDir(directory)

        directory = project_name + "/source/CMSIS/Device/ST/"
        directory += device_family + "/Source/iar/linker"
        MakeDir(directory)

        src = "CMSIS/Device/ST/" + device_family
        src += "/Include/" + device_family.lower() + ".h"
        dst = project_name + "/source/CMSIS/Device/ST/"
        dst += device_family + "/Include"
        CopyFile(src, dst)

        src = "CMSIS/Device/ST/" + device_family
        src += "/Include/" + device + ".h"
        dst = project_name + "/source/CMSIS/Device/ST/"
        dst += device_family + "/Include"
        CopyFile(src, dst)

        src = "CMSIS/Device/ST/" + device_family
        src += "/Include/system_" + device_family.lower() + ".h"
        dst = project_name + "/source/CMSIS/Device/ST/"
        dst += device_family + "/Include"
        CopyFile(src, dst)

        src = "CMSIS/Device/ST/" + device_family
        src += "/Source/Templates/" + "system_" + device_family.lower() + ".c"
        dst = project_name + "/source/CMSIS/Device/ST/"
        dst += device_family + "/Source"
        CopyFile(src, dst)

        src = "CMSIS/Device/ST/" + device_family
        src += "/Source/Templates/iar/" + "startup_" + device + ".s"
        dst = project_name + "/source/CMSIS/Device/ST/"
        dst += device_family + "/Source/iar"
        CopyFile(src, dst)

        src = "CMSIS/Device/ST/" + device_family
        src += "/Source/Templates/iar/linker/" + device + "_flash.icf"
        dst = project_name + "/source/CMSIS/Device/ST/"
        dst += device_family + "/Source/iar/linker"
        CopyFile(src, dst)

    else:
        Exit("Can not find \"CMSIS\" folder")

# Change template lines in project file
def ChangeProjectFile(project_name, device):
    device = device.lower()
    device_family = device[0:7].upper() + "xx"

    # Define project file path
    project_file = project_name + "/EWARM/" + project_name + ".ewp"

    # Define path to CMSIS device family folder
    CMSIS_ST_template_path = "$PROJ_DIR$\..\source\CMSIS\Device\ST\STM32F4xx"
    CMSIS_ST_path = "$PROJ_DIR$\..\source\CMSIS\Device\ST\\" + device_family

    # Repalce device definition
    text_to_replace = "STM32F407xx"
    replace_text = device.upper()[0:9] + device.lower()[9:]
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    # Replace CMSIS include path
    text_to_replace = CMSIS_ST_template_path + "\Include"
    replace_text = CMSIS_ST_path + "\Include"
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    # Replace linker path
    text_to_replace = CMSIS_ST_template_path
    text_to_replace += "\Source\iar\linker\stm32f407xx_flash.icf"
    replace_text = CMSIS_ST_path
    replace_text += "\Source\iar\linker\\" + device + "_flash.icf"
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    # Repalce folder and file paths
    text_to_replace = "<name>STM32F4xx</name>"
    replace_text = "<name>" + device_family + "</name>"
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    text_to_replace = CMSIS_ST_template_path + "\Include\stm32f407xx.h"
    replace_text = CMSIS_ST_path + "\Include\\" + device + ".h"
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    text_to_replace = CMSIS_ST_template_path + "\Include\stm32f4xx.h"
    replace_text = CMSIS_ST_path + "\Include\\" + device_family.lower() + ".h"
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    text_to_replace = CMSIS_ST_template_path + "\Include\system_stm32f4xx.h"
    replace_text = CMSIS_ST_path + "\Include\system_"
    replace_text += device_family.lower() + ".h"
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    text_to_replace = CMSIS_ST_template_path
    text_to_replace += "\Source\iar\linker\stm32f412rx_flash.icf"
    replace_text = CMSIS_ST_path +"\Source\iar\linker\\" + device + "_flash.icf"
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    text_to_replace = CMSIS_ST_template_path
    text_to_replace += "\Source\iar\startup_stm32f407xx.s"
    replace_text = CMSIS_ST_path + "\Source\iar\startup_" + device + ".s"
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    text_to_replace = CMSIS_ST_template_path + "\Source\system_stm32f4xx.c"
    replace_text = CMSIS_ST_path + "\Source\system_" + device_family + ".c"
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    # Define device core file
    device_f_series = device[6]
    if device_f_series == "0":
        device_core = "core_cm0.h"
    elif device_f_series == "1" or device_f_series == "2":
        device_core = "core_cm3.h"
    elif device_f_series == "3" or device_f_series == "4":
        device_core = "core_cm4.h"
    elif device_f_series == "7":
        device_core = "core_cm7.h"
    else:
        Exit("Can not define device core")

    text_to_replace = "$PROJ_DIR$\..\source\CMSIS\Include\core_cm4.h"
    replace_text = "$PROJ_DIR$\..\source\CMSIS\Include\\" + device_core
    ReplaceTextInFile(project_file, text_to_replace, replace_text)

    # Replace output .hex and .out files name
    ReplaceTextInFile(project_file, "template.hex", project_name + ".hex")
    ReplaceTextInFile(project_file, "tempalte.out", project_name + ".out")


# ------------------------------------------------------------------------------
# Copy folder to project source directory. Add folder in project file
# ------------------------------------------------------------------------------
def AddFolder(project_path, folder_path, ignore_list):
    if os.path.isfile(project_path):
        if project_path.endswith(".ewp"):
            if os.path.exists(folder_path):
                # Copy folder to project
                folder_path = DecoratePath(folder_path)
                src = folder_path
                dst = "/".join(project_path.split("/")[0:-2])
                dst += "/source/" + src.split("/")[-1]
                if os.path.exists(dst):
                    Exit("Folder \"" + dst + "\" exists")
                CopyTree(src, dst)

                # Add folder struct in project file
                tree = etree.parse(project_path)
                root = tree.getroot()

                start_path_pos = len(folder_path.split("/")) - 1
                elements = ParseFolder(folder_path, etree.Element("project"),
                                       ignore_list, start_path_pos, True)

                for node in elements:
                    text_node = etree.tostring(node, pretty_print = True)
                    root.append(etree.XML(text_node))

                xml_file = open(project_path, "wb")
                xml_file.write(etree.tostring(root, pretty_print = True,
                               encoding = "iso-8859-1", xml_declaration = True))
                xml_file.close()

            else:
                Exit("Can not find \"" + folder_path + "\" folder")
        else:
            Exit("\"" + project_path + "\" is not *.ewp file")
    else:
        Exit("Can not find: \"" + project_path + "\" file")


# Parse foder and add subfolders and files in XML tree
def ParseFolder(folder_path, parent_node, ignore_list,
                start_path_pos, first_entry):
    if first_entry:
        append_node = AppendNode("group", parent_node,
                                 folder_path.split("/")[-1])
    else:
        append_node = parent_node

    for item in os.listdir(folder_path):
        item_path = folder_path + "/" + item
        if os.path.isfile(item_path):
            path = "$PROJ_DIR$/../source/"
            path += "/".join(folder_path.split("/")[start_path_pos:])
            path += "/" + item

            if ignore_list != None:
                if not any(item.endswith(x) for x in ignore_list.split("/")):
                    AppendNode("file", append_node, path)
            else:
                AppendNode("file", append_node, path)
        else:
            sub_node = AppendNode("group", append_node, item)
            ParseFolder(item_path, sub_node, ignore_list, start_path_pos, False)

    return parent_node


# Append node in XML tree
def AppendNode(node_tag, parent_node, node_name):
    tag = etree.Element(node_tag)
    parent_node.append(tag)
    tag_name = etree.Element("name")
    tag_name.text = node_name
    tag.append(tag_name)

    return tag


# ------------------------------------------------------------------------------
# Clean workspace folder - delete all files and folders except *.eww and *.ewp
# ------------------------------------------------------------------------------
def Clean(workspace_path):
    if os.path.isfile(workspace_path):
        if workspace_path.endswith(".eww"):
            workspace_folder = workspace_path.split("/")[0:-1]
            workspace_folder = "/".join(workspace_folder)

            for item in os.listdir(workspace_folder):
                item_path = workspace_folder + item
                if os.path.isfile(item_path):
                    if not item.endswith(".eww") and not item.endswith(".ewp"):
                        try:
                            os.remove(item_path)
                        except OSError:
                            Exit("Can not delete \"" + item_path + "\" file")
                else:
                    try:
                        shutil.rmtree(item_path, True)
                    except IOError:
                        Exit("Can not delete \"" + item_path + "\" folder")

        else:
            Exit("\"" + workspace_path + "\" is not *.eww file")
    else:
        Exit("Can not find: \"" + workspace_path + "\" file")


# ------------------------------------------------------------------------------
# Rename workspace with specified name
# ------------------------------------------------------------------------------
def RenameWorkspace(workspace_path, new_workspace_name):
    if os.path.isfile(workspace_path):
        if workspace_path.endswith(".eww"):
            rename_path = workspace_path.split("/")
            rename_path[-1] = new_workspace_name + ".eww"
            rename_path = "/".join(rename_path)
            try:
                os.rename(workspace_path, rename_path)
            except OSError:
                Exit("Can not rename \"" + workspace_path + "\" file")
        else:
            Exit("\"" + workspace_path + "\" is not *.eww file")
    else:
        Exit("Can not find: \"" + workspace_path + "\" file")


# ------------------------------------------------------------------------------
# Rename project with specified name
# ------------------------------------------------------------------------------
def RenameProject(project_path, workspace_path, new_project_name):
    if os.path.isfile(project_path):
        if os.path.isfile(workspace_path):
            if project_path.endswith(".ewp"):
                if workspace_path.endswith(".eww"):

                    rename_path = project_path.split("/")
                    old_project_name = rename_path[-1]
                    rename_path[-1] = new_project_name + ".ewp"
                    rename_path = "/".join(rename_path)
                    try:
                        os.rename(project_path, rename_path)
                    except OSError:
                        Exit("Can non rename \"" + project_path + "\" file")

                    text_to_replace = "$WS_DIR$\\" + old_project_name
                    replace_text = "$WS_DIR$\\" + new_project_name + ".ewp"
                    ReplaceTextInFile(workspace_path, text_to_replace,
                                      replace_text)

                else:
                    Exit("\"" + workspace_path + "\" is not *.eww file")
            else:
                Exit("\"" + project_path + "\" is not *.ewp file")
        else:
            Exit("Can not find: \"" + workspace_path + "\" file")
    else:
        Exit("Can not find: \"" + project_path + "\" file")




# ------------------------------------------------------------------------------
# Common functions
# ------------------------------------------------------------------------------
# Replace text in file
def ReplaceTextInFile(file_name, text_to_replace, replace_text):
    if os.path.exists(file_name):
        try:
            file = open(file_name, "r")
            text = file.read()
            file.close()
            file = open(file_name, "w")
            file.write(text.replace(text_to_replace, replace_text))
            file.close()
        except IOError:
            Exit("Can not handle \"" + file_name + "\" file")
    else:
        Exit("Can not find \"" + file_name + "\" file")


# Copy folder tree
def CopyTree(src, dst, symlinks = False, ignore = None):
    if not os.path.exists(dst):
        MakeDir(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
            except IOError:
                Exit("Can not copy \"" + s + "\" folder")
        else:
            CopyFile(s, d)


# Make directory
def MakeDir(directory):
    try:
        os.makedirs(directory)
    except OSError:
        Exit("Can not create \"" + directory + "\" folder")


# Copy file
def CopyFile(src, dst):
    try:
        shutil.copy2(src, dst)
    except IOError:
        Exit("Can not copy \"" + src + "\"")


# Decorate path to next template "folder/subfolder/file.xxx"
def DecoratePath(path):
    if path.endswith("/"):
        path = "/".join(path.split("/")[0:-1])
    if path.startswith("./"):
        path = "/".join(path.split("/")[1:])

    return path


# Print message and exit
def Exit(exit_message):
    print(exit_message)
    exit(1)




# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    arg_parser = CreateArgParser()
    arg_parser_namespace = arg_parser.parse_args()

    # Create command
    if arg_parser_namespace.command == "create":
        if (arg_parser_namespace.help == True or
            arg_parser_namespace.name == None or
            arg_parser_namespace.device == None):
            Exit(CREATE_HELP_MESSAGE)
        else:
            Create(arg_parser_namespace.name, arg_parser_namespace.device)

    # Add folder command
    elif arg_parser_namespace.command == "add_folder":
        if (arg_parser_namespace.help == True or
            arg_parser_namespace.project_path == None or
            arg_parser_namespace.folder_path == None):
            Exit(ADD_FOLDER_HELP_MESSAGE)
        else:
            AddFolder(arg_parser_namespace.project_path,
                      arg_parser_namespace.folder_path,
                      arg_parser_namespace.ignore)

    # Clean command
    elif arg_parser_namespace.command == "clean":
        if (arg_parser_namespace.help == True or
            arg_parser_namespace.workspace_path == None):
            Exit(CLEAN_HELP_MESSAGE)
        else:
            Clean(arg_parser_namespace.workspace_path)

    # Rename workspace command
    elif arg_parser_namespace.command == "rename_workspace":
        if (arg_parser_namespace.help == True or
            arg_parser_namespace.workspace_path == None or
            arg_parser_namespace.name == None):
            Exit(RENAME_WORKSPACE_HELP_MESSAGE)
        else:
            RenameWorkspace(arg_parser_namespace.workspace_path,
                            arg_parser_namespace.name)

    # Rename project command
    elif arg_parser_namespace.command == "rename_project":
        if (arg_parser_namespace.help == True or
            arg_parser_namespace.project_path == None or
            arg_parser_namespace.workspace_path == None or
            arg_parser_namespace.name == None):
            Exit(RENAME_PROJECT_HELP_MESSAGE)
        else:
            RenameProject(arg_parser_namespace.project_path,
                          arg_parser_namespace.workspace_path,
                          arg_parser_namespace.name)

    # Rename command
    elif arg_parser_namespace.command == "rename":
        if (arg_parser_namespace.help == True or
            arg_parser_namespace.project_path == None or
            arg_parser_namespace.workspace_path == None or
            arg_parser_namespace.name == None):
            Exit(RENAME_HELP_MESSAGE)
        else:
            RenameProject(arg_parser_namespace.project_path,
                          arg_parser_namespace.workspace_path,
                          arg_parser_namespace.name)
            RenameWorkspace(arg_parser_namespace.workspace_path,
                            arg_parser_namespace.name)

    # Undefined command
    else:
        Exit(MAIN_HELP_MESSAGE)

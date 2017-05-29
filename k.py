# -*- coding: utf8 -*-

import c4d

# constants

TITLE = "Automatic FBX Exporter"

MAIN_COMMAND_PLUGIN_ID = 1039303
MAIN_COMMAND_NAME = "#$1 Do FBX save"
MAIN_COMMAND_HELP = "A plug in that automates exporting as FBX"

TOGGLE_DO_SAVE_COMMAND_PLUGIN_ID = 1039304
TOGGLE_DO_SAVE_COMMAND_NAME = "#$3 Do Cinema 4D “Save” command"
TOGGLE_DO_SAVE_COMMAND_HELP = "Does a standard Cinema 4D save command"

GET_PATH_PLUGIN_ID = 1039305
GET_PATH_NAME = "#$2 Set FBX export path…"
GET_PATH_HELP = "Specify the path for the exported FBX"

# base container

PATH_FOR_FBX = 1

# various options/flags used with c4d.documents.SaveDocument in "Export" method

C4D_OPTION_SAVE_AS_FBX = 1026370

# command codes ( for use with c4d.CallCommand )

COMMAND_SAVE = 12098

# preferences ( c4d.plugins.GetWorldPluginData )

PREF_DO_C4D_SAVE_COMMAND = 1
PREF_PREVIOUS_PATH = 2

# miscellaneous

NEWLINE = "\n"

# dialog box

LBL_INFO_CURRENT = 1000
TXT_PATH_CURRENT = 1001

LBL_INFO_NEW = 1002
TXT_PATH_NEW = 1003

BTN_SELECT = 1004

NEW_PATH_GROUP_OPTIONS = 3000

GROUP_OPTIONS = 2000
BTN_OK = 2001
BTN_CANCEL = 2002


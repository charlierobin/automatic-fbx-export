# automatic-fbx-export
Automates saving a Cinema 4D document and simultaneously exporting an FBX version to another path

If you put Cinema 4D files into a Unity asset directort, Unity basically fires up a behind-the-scenes command line version of Cinema 4D and uses it to export an FBX out of your C4D file.

Under some circumstances it can be preferable to have the Cinema 4D file elsewhere on your filesystem, and to export the FBXs into the Unity directory yourself.

This plug-in makes that a little easier.

You specify a path/name for the FBX file, and then when you run the command, the FBX is exported.

The “Do Cinema 4D save” option makes the plug-in carry out a standard Cinema 4D save before carrying out the actual export. This allows you to assign the standard command-S/control-S keyboard shortcut to the plug-in, where it will still behave as you would expect it to, with the added benefit of getting your FBX saved out as well.

Uses the Cinema 4D Python SDK:

https://developers.maxon.net/docs/Cinema4DPythonSDK/html/index.html

***********************

There is NO copyright or license for this code, please help yourself and do what you like with it. (Although it would be nice if any use were acknowledged, and any improvements/fixes you made were shared back for the benefit of everyone, it is not required.)

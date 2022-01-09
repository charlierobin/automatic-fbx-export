import c4d, os, sys
from c4d import plugins, utils, documents, gui, bitmaps, storage

folder = os.path.dirname( __file__ )
if folder not in sys.path: sys.path.insert( 0, folder )

import k

class OptionsDialog( gui.GeDialog ):
    
    def __init__( self, defaultString, currentString ):
        
        self.defaultString = defaultString
        self.currentString = currentString
        self.path = ""
        self.wasOkayed = False
    
        if self.currentString == "": self.currentString = "(nothing)"
        
    def CreateLayout( self ):
        
        self.SetTitle( k.TITLE )
        
        self.AddStaticText( k.LBL_INFO_CURRENT, c4d.BFH_LEFT, name = "Currently set to:" )
        self.AddStaticText( k.TXT_PATH_CURRENT, c4d.BFH_SCALEFIT, name = self.currentString, borderstyle = c4d.BORDER_THIN_IN )
        
        self.AddStaticText( 0, c4d.BFH_LEFT, name = " " ) 
        
        self.AddStaticText( k.LBL_INFO_NEW, c4d.BFH_LEFT, name = "New path:" ) 
        self.AddStaticText( k.TXT_PATH_NEW, c4d.BFH_SCALEFIT, name = self.defaultString, borderstyle = c4d.BORDER_THIN_IN )
        
        self.AddButton( k.BTN_SELECT, c4d.BFH_LEFT, name = "   Select…   " )

        self.AddStaticText( 0, c4d.BFH_LEFT, name = " " ) 

        self.GroupBegin( k.GROUP_OPTIONS, c4d.BFH_RIGHT, 2, 1 )
        self.AddButton( k.BTN_CANCEL, c4d.BFH_SCALE, name = "   Cancel   " )
        self.AddButton( k.BTN_OK, c4d.BFH_SCALE, name = "        OK        " )
        self.GroupEnd()
        
        return True

    def Command( self, id, msg ):
        
        if id == k.BTN_CANCEL:
            
            self.wasOkayed = False
            self.Close()
            
        elif id == k.BTN_OK:
            
            self.wasOkayed = True
            self.path = self.GetString( k.TXT_PATH_NEW )
            self.Close()
        
        elif id == k.BTN_SELECT:
            
            returnedPath = c4d.storage.SaveDialog( c4d.FILESELECTTYPE_ANYTHING, "Export where?", "fbx", self.defaultString )
            if returnedPath is not None: self.SetString( k.TXT_PATH_NEW, returnedPath )
            
        return True
    
class ToggleDoSave( plugins.CommandData ):
    
    def Execute( self, doc ):
        
        preferences = GetPreferences()
        preferences.SetBool( k.PREF_DO_C4D_SAVE_COMMAND, not preferences.GetBool( k.PREF_DO_C4D_SAVE_COMMAND ) )
        
        return True
    
    def GetState( self, doc ):
        
        preferences = GetPreferences()
        
        if preferences.GetBool( k.PREF_DO_C4D_SAVE_COMMAND ):
            return c4d.CMD_ENABLED | c4d.CMD_VALUE
        else:
            return c4d.CMD_ENABLED

class GetPath( plugins.CommandData ):
    
    def Execute( self, doc ):
        
        documentBaseContainer = GetDocumentPluginData( doc )
        
        defaultString = documentBaseContainer[ k.PATH_FOR_FBX ]
        currentString = documentBaseContainer[ k.PATH_FOR_FBX ]
        
        if defaultString == "":
            
            defaultString = doc.GetDocumentName()
            defaultString, extension = os.path.splitext( defaultString )
            defaultString = defaultString + ".fbx"
            defaultString = os.path.join( storage.GeGetC4DPath( c4d.C4D_PATH_DESKTOP ), defaultString )
        
        dialog = OptionsDialog( defaultString, currentString )
        dialog.Open( c4d.DLG_TYPE_MODAL, defaultw = 350, defaulth = 70 )
        
        if dialog.wasOkayed: documentBaseContainer[ k.PATH_FOR_FBX ] = dialog.path

        return True
    
class AutomaticFBXExport( plugins.CommandData ):
    
    def Execute( self, doc ):

        documentBaseContainer = GetDocumentPluginData( doc )
        path = documentBaseContainer[ k.PATH_FOR_FBX ]

        if path is None or path == "":
            gui.MessageDialog( "Please specifiy a path for your FBX export." )
            return True
        
        testPath, filename = os.path.split( path )
        
        if not os.path.exists( testPath ):
            gui.MessageDialog( "The export path does not exist." )
            return True
        
        preferences = GetPreferences()
        if preferences.GetBool( k.PREF_DO_C4D_SAVE_COMMAND ): c4d.CallCommand( k.COMMAND_SAVE )

        c4d.documents.SaveDocument( doc, path, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, k.C4D_OPTION_SAVE_AS_FBX )
        
        return True

def GetDocumentPluginData( doc ):
    
    bc = doc.GetDataInstance().GetContainerInstance( k.MAIN_COMMAND_PLUGIN_ID )

    if bc is None:
        
        bc = c4d.BaseContainer()
        bc[ k.PATH_FOR_FBX ] = ""
        doc[ k.MAIN_COMMAND_PLUGIN_ID ] = bc
        
        bc = doc.GetDataInstance().GetContainerInstance( k.MAIN_COMMAND_PLUGIN_ID )
        
    return bc
            
def GetPreferences():
    
    preferences = c4d.plugins.GetWorldPluginData( k.MAIN_COMMAND_PLUGIN_ID )
    
    if preferences == None:

        preferences = c4d.BaseContainer()
        result = c4d.plugins.SetWorldPluginData( k.MAIN_COMMAND_PLUGIN_ID, preferences )

    if preferences.GetBool( k.PREF_DO_C4D_SAVE_COMMAND ) == None: preferences.SetBool( k.PREF_DO_C4D_SAVE_COMMAND, False )
    
    return preferences

if __name__ == "__main__":

    theBitmap = bitmaps.BaseBitmap()
    
    theDirectoryPath, theFileName = os.path.split( __file__ )

    theBitmap.InitWith( os.path.join( theDirectoryPath, "res", "icon.tif" ) )

    plugins.RegisterCommandPlugin( id = k.MAIN_COMMAND_PLUGIN_ID, 
                                   str = k.MAIN_COMMAND_NAME, 
                                   info = 0, 
                                   icon = theBitmap, 
                                   help = k.MAIN_COMMAND_HELP, 
                                   dat = AutomaticFBXExport() )
    
    plugins.RegisterCommandPlugin( id = k.TOGGLE_DO_SAVE_COMMAND_PLUGIN_ID, 
                                   str = k.TOGGLE_DO_SAVE_COMMAND_NAME, 
                                   info = 0, 
                                   icon = None, 
                                   help = k.TOGGLE_DO_SAVE_COMMAND_HELP, 
                                   dat = ToggleDoSave() )
    
    plugins.RegisterCommandPlugin( id = k.GET_PATH_PLUGIN_ID, 
                                   str = k.GET_PATH_NAME, 
                                   info = 0, 
                                   icon = None, 
                                   help = k.GET_PATH_HELP, 
                                   dat = GetPath() )
    
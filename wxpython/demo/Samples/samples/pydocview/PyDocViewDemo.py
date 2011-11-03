#----------------------------------------------------------------------------
# Name:         PyDocViewDemo.py
# Purpose:      Demo of Python extensions to the wxWindows docview framework
#
# Author:       Peter Yared, Morgan Hua
#
# Created:      5/15/03
# CVS-ID:       $Id: PyDocViewDemo.py 36607 2005-12-30 23:02:03Z RD $
# Copyright:    (c) 2003-2005 ActiveGrid, Inc.
# License:      wxWindows License
#----------------------------------------------------------------------------


import sys
import os.path
import wx
import wx.lib.docview as docview
import wx.lib.pydocview as pydocview
import TextEditor
import FindService
_ = wx.GetTranslation


#----------------------------------------------------------------------------
# Classes
#----------------------------------------------------------------------------

class TextEditorApplication(pydocview.DocApp):

    SPLASH = "splash.png"
    
    def OnInit(self):
        # Call the super - this is important!!!
        pydocview.DocApp.OnInit(self)

        # Show the splash dialog while everything is loading up
        if os.path.exists(TextEditorApplication.SPLASH):
            self.ShowSplash(TextEditorApplication.SPLASH)

        # Set the name and the icon
        self.SetAppName(_("wxPython PyDocView Demo"))
        self.SetDefaultIcon(pydocview.getBlankIcon())
        
        # Initialize the document manager
        docManager = docview.DocManager(flags = self.GetDefaultDocManagerFlags())  
        self.SetDocumentManager(docManager)

        # Create a template for text documents and associate it with the docmanager
        textTemplate = docview.DocTemplate(docManager,
                                              _("Text"),
                                              "*.text;*.txt",
                                              _("Text"),
                                              _(".txt"),
                                              _("Text Document"),
                                              _("Text View"),
                                              TextEditor.TextDocument,
                                              TextEditor.TextView,
                                              icon=pydocview.getBlankIcon())
        docManager.AssociateTemplate(textTemplate)

        # Install services - these can install menu and toolbar items
        textService           = self.InstallService(TextEditor.TextService())
        findService           = self.InstallService(FindService.FindService())
        optionsService        = self.InstallService(pydocview.DocOptionsService(supportedModes=wx.lib.docview.DOC_MDI))
        windowMenuService     = self.InstallService(pydocview.WindowMenuService())
        filePropertiesService = self.InstallService(pydocview.FilePropertiesService())
        if os.path.exists(TextEditorApplication.SPLASH):
            aboutService      = self.InstallService(pydocview.AboutService(image=wx.Image(TextEditorApplication.SPLASH)))
        else:
            aboutService      = self.InstallService(pydocview.AboutService())
            
        # Install the TextEditor's option panel into the OptionsService
        optionsService.AddOptionsPanel(TextEditor.TextOptionsPanel)

        # If it is an MDI app open the main frame
        self.OpenMainFrame()
        
        # Open any files that were passed via the command line
        self.OpenCommandLineArgs()
        
        # If nothing was opened and it is an SDI app, open up an empty text document
        if not docManager.GetDocuments() and docManager.GetFlags() & wx.lib.docview.DOC_SDI:
            textTemplate.CreateDocument('', docview.DOC_NEW).OnNewDocument()

        # Close the splash dialog
        if os.path.exists(TextEditorApplication.SPLASH):
            self.CloseSplash()
        
        # Show the tips dialog
        if os.path.exists("tips.txt"):
            wx.CallAfter(self.ShowTip, wx.GetApp().GetTopWindow(), wx.CreateFileTipProvider("tips.txt", 0))

        wx.UpdateUIEvent.SetUpdateInterval(1000)  # Overhead of updating menus was too much.  Change to update every N milliseconds.

        # Tell the framework that everything is great
        return True


#----------------------------------------------------------------------------
# Main
#----------------------------------------------------------------------------

# Run the TextEditorApplication and do not redirect output to the wxPython error dialog
app = TextEditorApplication(redirect=False)
app.MainLoop()

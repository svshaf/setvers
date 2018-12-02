# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Aug  8 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class GUIFrame
###########################################################################

class GUIFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Version Info", pos = wx.DefaultPosition, size = wx.Size( 671,276 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel3 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.st_Directory = wx.StaticText( self.m_panel3, wx.ID_ANY, u"Project Directory:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.st_Directory.Wrap( -1 )
		
		bSizer3.Add( self.st_Directory, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 10 )
		
		ch_DirectoryChoices = []
		self.ch_Directory = wx.Choice( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ch_DirectoryChoices, 0 )
		self.ch_Directory.SetSelection( 0 )
		bSizer3.Add( self.ch_Directory, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, 10 )
		
		self.bt_SelectDir = wx.Button( self.m_panel3, wx.ID_ANY, u"Select", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.bt_SelectDir, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 10 )
		
		
		self.m_panel3.SetSizer( bSizer3 )
		self.m_panel3.Layout()
		bSizer3.Fit( self.m_panel3 )
		bSizer7.Add( self.m_panel3, 0, wx.EXPAND |wx.ALL, 0 )
		
		self.pn_Main = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer2 = wx.GridSizer( 4, 4, 0, 0 )
		
		self.st_Version = wx.StaticText( self.pn_Main, wx.ID_ANY, u"Version:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.st_Version.Wrap( -1 )
		
		gSizer2.Add( self.st_Version, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10 )
		
		self.et_Version = wx.TextCtrl( self.pn_Main, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.et_Version, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		self.st_VersionPrev = wx.StaticText( self.pn_Main, wx.ID_ANY, u"[version]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.st_VersionPrev.Wrap( -1 )
		
		gSizer2.Add( self.st_VersionPrev, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.bt_IncVersion = wx.Button( self.pn_Main, wx.ID_ANY, u"Incr.Version", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.bt_IncVersion, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL, 7 )
		
		self.st_Build = wx.StaticText( self.pn_Main, wx.ID_ANY, u"Build:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.st_Build.Wrap( -1 )
		
		gSizer2.Add( self.st_Build, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10 )
		
		self.et_Build = wx.TextCtrl( self.pn_Main, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.et_Build, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		self.st_BuildPrev = wx.StaticText( self.pn_Main, wx.ID_ANY, u"[build]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.st_BuildPrev.Wrap( -1 )
		
		gSizer2.Add( self.st_BuildPrev, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		gSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.st_Created = wx.StaticText( self.pn_Main, wx.ID_ANY, u"Created:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.st_Created.Wrap( -1 )
		
		gSizer2.Add( self.st_Created, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 10 )
		
		self.et_Created = wx.TextCtrl( self.pn_Main, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.et_Created, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		self.st_CreatedPrev = wx.StaticText( self.pn_Main, wx.ID_ANY, u"[created]", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.st_CreatedPrev.Wrap( -1 )
		
		gSizer2.Add( self.st_CreatedPrev, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		gSizer2.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.bt_Set = wx.Button( self.pn_Main, wx.ID_ANY, u"Set", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.bt_Set, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10 )
		
		self.bt_Revert = wx.Button( self.pn_Main, wx.ID_ANY, u"Revert", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.bt_Revert, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, 5 )
		
		
		gSizer2.Add( ( 0, 0), 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		gSizer2.Add( ( 0, 0), 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		
		self.pn_Main.SetSizer( gSizer2 )
		self.pn_Main.Layout()
		gSizer2.Fit( self.pn_Main )
		bSizer7.Add( self.pn_Main, 1, wx.EXPAND|wx.LEFT, 0 )
		
		self.pn_StatusBar = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.st_Status = wx.StaticText( self.pn_StatusBar, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.st_Status.Wrap( -1 )
		
		bSizer2.Add( self.st_Status, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		self.pn_StatusBar.SetSizer( bSizer2 )
		self.pn_StatusBar.Layout()
		bSizer2.Fit( self.pn_StatusBar )
		bSizer7.Add( self.pn_StatusBar, 0, wx.ALL|wx.EXPAND, 0 )
		
		
		self.SetSizer( bSizer7 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.MainFrame_OnClose )
		self.ch_Directory.Bind( wx.EVT_CHOICE, self.ch_Directory_OnChoice )
		self.bt_SelectDir.Bind( wx.EVT_BUTTON, self.bt_SelectDir_OnClick )
		self.bt_IncVersion.Bind( wx.EVT_BUTTON, self.bt_IncVersion_OnClick )
		self.bt_Set.Bind( wx.EVT_BUTTON, self.bt_Set_OnClick )
		self.bt_Revert.Bind( wx.EVT_BUTTON, self.bt_Revert_OnClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def MainFrame_OnClose( self, event ):
		event.Skip()
	
	def ch_Directory_OnChoice( self, event ):
		event.Skip()
	
	def bt_SelectDir_OnClick( self, event ):
		event.Skip()
	
	def bt_IncVersion_OnClick( self, event ):
		event.Skip()
	
	def bt_Set_OnClick( self, event ):
		event.Skip()
	
	def bt_Revert_OnClick( self, event ):
		event.Skip()
	


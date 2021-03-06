#!/usr/bin/env python3

#  ----------------------------------------------------------------------------
# Name:         setvers.py
# Purpose:      Update version info in headers of project's .py files
#
# Author:       Sergey Shafranskiy <sergey.shafranskiy@gmail.com>
#
# Version:      1.1.0
# Build:        41
# Created:      2018-12-04
#  ----------------------------------------------------------------------------

import wx
import os
import re
import configparser as cp
from datetime import datetime as dt

import setvers_gui

# .vers file constants

CFG_SEC_CURVERS = 'Current Version'
CFG_OPT_AUTHOR = 'Author'
CFG_OPT_VERSION = 'Version'
CFG_OPT_BUILD = 'Build'
CFG_OPT_CREATED = 'Created'

# Initial values

CFG_DEF_AUTHOR = 'Specify author name, E-Mail'
CFG_DEF_VERSION = '1.0.0'
CFG_DEF_BUILD = '1'

# .ini file constants

INI_SEC_HISTORY = 'History'
INI_OPT_COUNT = 'Count'

# Max count of directories in history

MAX_DIR_COUNT = 15


class MainFrame(setvers_gui.GUIFrame):
    """
    Main Frame
    """

    def __init__(self, parent):
        """
        Class constructor
        """
        super(MainFrame, self).__init__(parent)

        self.pfname_module = __file__.rsplit(".", 1)[0]  # pathname of running module

        self.path = None  # Current directory
        self.pfname_vers = None  # Pathname of the .vers file in current directory
        self.pfnames_py = []  # List of pathnames of .py files in current directory

        # set application's icon
        icon = wx.Icon(self.pfname_module + ".ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Read configuration from .ini file
        self.pfname_ini = self.pfname_module + ".ini"  # Pathname of .ini file
        self.read_ini()

        # Read version info from .vers file from project directory
        self.read_vers(self.ch_Directory.GetString(0))
        return

    def MainFrame_OnClose(self, event):
        """
        Close window

        :param event:
        :return:
        """
        self.save_ini()  # Save settings
        event.Skip()
        return

    def read_ini(self):
        """
        # Read configuration from .ini file

        :return:
        """
        ini_cfg = cp.ConfigParser()
        ini_cfg.read(self.pfname_ini)

        count = ini_cfg.getint(INI_SEC_HISTORY, INI_OPT_COUNT)
        if count is None:
            hist = [self.pfname_module]
        else:
            hist = [ini_cfg.get(INI_SEC_HISTORY, str(i)) for i in range(count)]

        self.ch_Directory.AppendItems(hist)
        self.ch_Directory.SetSelection(0)
        return

    def save_ini(self):
        """
        Save configuration to .ini file

        :return:
        """
        ini_cfg = cp.ConfigParser()

        ini_cfg.add_section(INI_SEC_HISTORY)
        count = self.ch_Directory.GetCount()
        if count > MAX_DIR_COUNT:
            count = MAX_DIR_COUNT
        ini_cfg.set(INI_SEC_HISTORY, INI_OPT_COUNT, str(count))
        for i in range(count):
            ini_cfg.set(INI_SEC_HISTORY, str(i), self.ch_Directory.GetString(i))

        with open(self.pfname_ini, 'w') as cf:
            ini_cfg.write(cf)
        return

    def read_vers(self, path):
        """
        # Read version info from .vers file in current directory

        :param path: Path to project directory with .vers file
        :return:
        """
        self.path = path
        self.pfname_vers = os.path.join(self.path, '.vers')

        self.pfnames_py = [os.path.abspath(os.path.join(self.path, pfname)) for pfname in os.listdir(self.path)
                           if os.path.isfile(os.path.join(self.path, pfname)) and
                           (os.path.splitext(pfname)[1] == '.py')]
        self.st_Status.SetLabel('{} .py file(s) found in {}'.format(len(self.pfnames_py), self.path))

        self.ver_cfg = cp.ConfigParser()  # Version config. class instance
        self.ver_cfg.optionxform = str

        if not os.path.exists(self.pfname_vers):  # if .vers file doesn't exists
            # create new .vers file
            self.ver_cfg.add_section(CFG_SEC_CURVERS)
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_AUTHOR, CFG_DEF_AUTHOR)
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_VERSION, CFG_DEF_VERSION)
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_BUILD, CFG_DEF_BUILD)
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_CREATED, dt.now().strftime('%Y-%m-%d'))

            with open(self.pfname_vers, 'w') as cf:
                self.ver_cfg.write(cf)
        else:
            self.ver_cfg.read(self.pfname_vers)  # load version info from .vers file

        author = self.ver_cfg.get(CFG_SEC_CURVERS, CFG_OPT_AUTHOR, fallback=CFG_DEF_AUTHOR)
        vers = self.ver_cfg.get(CFG_SEC_CURVERS, CFG_OPT_VERSION, fallback=CFG_DEF_VERSION)
        build = self.ver_cfg.get(CFG_SEC_CURVERS, CFG_OPT_BUILD, fallback=CFG_DEF_BUILD)
        created = self.ver_cfg.get(CFG_SEC_CURVERS, CFG_OPT_CREATED, fallback=dt.now().strftime('%Y-%m-%d'))

        vers_new = vers
        build_new = str(int(build) + 1)
        created_new = dt.now().strftime('%Y-%m-%d')

        self.et_Author.SetValue(author)
        self.et_Version.SetValue(vers_new)
        self.st_VersionPrev.SetLabel(vers)
        self.et_Build.SetValue(build_new)
        self.st_BuildPrev.SetLabel(build)
        self.et_Created.SetValue(created_new)
        self.st_CreatedPrev.SetLabel(created)

        #  Regex patterns for replaced strings in .py file header
        self.pc = []
        self.pc.append(re.compile(r'(^# Name:\s+)(.*?$)', flags=re.MULTILINE | re.S))  # name of module
        self.pc.append(re.compile(r'(^# Author:\s+)(.*?$)', flags=re.MULTILINE | re.S))  # author info
        # version info
        self.pc.append(re.compile(r'(^# Version:\s+)(\d.*?$)', flags=re.MULTILINE | re.S))
        self.pc.append(re.compile(r'(^# Build:\s+)(\d.*?$)', flags=re.MULTILINE | re.S))
        self.pc.append(re.compile(r'(^# Created:\s+)(\d{4}-\d{2}-\d{2}.*?$)', flags=re.MULTILINE | re.S))
        return

    def save_vers(self):
        """
        Save version info to .vers file in current directory

        :return:
        """
        if self.pfname_vers is not None:
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_VERSION, self.et_Version.GetValue())
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_BUILD, self.et_Build.GetValue())
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_CREATED, self.et_Created.GetValue())
            with open(self.pfname_vers, 'w') as cf:
                self.ver_cfg.write(cf)
        return

    def ch_Directory_OnChoice(self, event):
        """
        Select directory in choice list

        :param event:
        :return:
        """
        index = self.ch_Directory.GetSelection()
        if index != 0:
            value = self.ch_Directory.GetString(index)
            self.ch_Directory.Delete(index)
            self.ch_Directory.Insert(value, 0)
            self.ch_Directory.SetSelection(0)
            self.read_vers(value)
        return

    def bt_SelectDir_OnClick(self, event):
        """
        Choose new directory

        :param event:
        :return:
        """
        with wx.DirDialog(None, "Choose Project Directory", self.path,
                          wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                value = dlg.GetPath()

                # Check if directory already in choice list
                index = -1
                for i in range(self.ch_Directory.GetCount()):
                    if self.ch_Directory.GetString(i) == value:
                        index = i
                        break
                if index == -1:
                    # Add directory to choice list
                    index = 0
                    self.ch_Directory.Insert(value, 0)

                self.ch_Directory.SetSelection(index)
                self.read_vers(value)
        return

    def bt_Set_OnClick(self, event):
        """
        Apply new version info to all .py files in current directory

        :param event:
        :return:
        """
        self.update_py_files(['$MODULE_NAME', '$AUTHOR',
                              self.et_Version.GetValue(),
                              self.et_Build.GetValue(),
                              self.et_Created.GetValue()])
        return

    def bt_Revert_OnClick(self, event):
        """
        Restore previous version info in all .py files in current directory

        :param event:
        :return:
        """
        self.update_py_files(['$MODULE_NAME', '$AUTHOR',
                              self.st_VersionPrev.GetLabel(),
                              self.st_BuildPrev.GetLabel(),
                              self.st_CreatedPrev.GetLabel()])
        return

    def update_py_files(self, vals: list):
        """
        Update version info in all .py files

        :param vals: Values to replace
        :return:
        """
        for pfname in self.pfnames_py:
            self.st_Status.SetLabel('Updating file {}'.format(pfname))
            self.st_Status.Update()
            with open(pfname, "r") as f:
                text = f.read()

                n_updates = 0
                for i, v in enumerate(vals):
                    if v == '$MODULE_NAME':  # replace module name
                        v = os.path.basename(pfname)
                    elif v == '$AUTHOR':  # replace author info
                        v = self.et_Author.GetValue()

                    text, n = re.subn(self.pc[i], r'\g<1>' + v, text, count=1)
                    n_updates += n

            if n_updates > 0:  # if text was changed
                with open(pfname, "w") as f:
                    f.write(text)

        self.st_Status.SetLabel('{} .py file(s) updated in {}'.format(len(self.pfnames_py), self.path))

        # Save new values to .vers file
        self.save_vers()
        return

    def bt_IncVersion_OnClick(self, event):
        """
        Increment last number ZZ in version XX.YY.ZZ

        :param event:
        :return:
        """
        vers = self.et_Version.GetValue()
        vs = vers.rsplit(".", 1)
        vers_new = vs[0] + '.' + str(int(vs[1]) + 1)
        self.et_Version.SetValue(vers_new)
        return


def main():
    app = wx.App(False)
    frame = MainFrame(None)
    frame.CenterOnScreen()
    frame.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    main()

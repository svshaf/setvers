#!/usr/bin/env python3

#  ----------------------------------------------------------------------------
# Name:         setvers.py
# Purpose:      Update version info in headers of project's .py files
#
# Author:       Sergey Shafranskiy <sergey.shafranskiy@gmail.com>
#
# Version:      1.1
# Build:        35
# Created:      2018-12-02
#  ----------------------------------------------------------------------------

import wx
import os
import re
import configparser as cp
from datetime import datetime as dt

import setvers_gui

CFG_SEC_CURVERS = 'Current Version'
CFG_OPT_VERSION = 'Version'
CFG_OPT_BUILD = 'Build'
CFG_OPT_CREATED = 'Created'

INI_SEC_HISTORY = 'History'
INI_OPT_COUNT = 'Count'


class MainFrame(setvers_gui.GUIFrame):

    def __init__(self, parent):
        """
        Class constructor
        """
        super(MainFrame, self).__init__(parent)

        self.pfname_module = __file__.rsplit(".", 1)[0]  # pathname of running module

        self.path = None
        self.pfname_vers = None
        self.pfnames_py = []

        # set window's icon
        icon = wx.Icon(self.pfname_module + ".ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Read configuration from .ini file
        self.pfname_ini = self.pfname_module + ".ini"
        self.read_ini()

        # Read version info from .vers file from project directory
        self.read_vers(self.ch_Directory.GetString(0))
        return

    def MainFrame_OnClose(self, event):
        self.save_ini()
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
        ini_cfg = cp.ConfigParser()

        ini_cfg.add_section(INI_SEC_HISTORY)
        count = self.ch_Directory.GetCount()
        ini_cfg.set(INI_SEC_HISTORY, INI_OPT_COUNT, str(count))
        for i in range(count):
            ini_cfg.set(INI_SEC_HISTORY, str(i), self.ch_Directory.GetString(i))

        with open(self.pfname_ini, 'w') as cf:
            ini_cfg.write(cf)
        return

    def read_vers(self, path):
        """
        # Read version info from .vers file from project directory
        :param path: Project directory with .vers file
        :return:
        """
        self.path = path
        self.pfname_vers = os.path.join(self.path, '.vers')

        self.pfnames_py = [os.path.abspath(os.path.join(self.path, fn)) for fn in os.listdir(self.path)
                           if os.path.isfile(os.path.join(self.path, fn)) and (os.path.splitext(fn)[1] == '.py')]
        self.st_Status.SetLabel('{} .py file(s) found in {}'.format(len(self.pfnames_py), self.path))

        self.ver_cfg = cp.ConfigParser()
        self.ver_cfg.optionxform = str
        if not os.path.exists(self.pfname_vers):
            self.ver_cfg.add_section(CFG_SEC_CURVERS)
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_VERSION, '1.0.0')
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_BUILD, '1')
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_CREATED, dt.now().strftime('%Y-%m-%d'))
            # cfg['Version History'] = {}

            with open(self.pfname_vers, 'w') as cf:
                self.ver_cfg.write(cf)
        else:
            self.ver_cfg.read(self.pfname_vers)

        vers = self.ver_cfg.get(CFG_SEC_CURVERS, CFG_OPT_VERSION)
        build = self.ver_cfg.get(CFG_SEC_CURVERS, CFG_OPT_BUILD)
        created = self.ver_cfg.get(CFG_SEC_CURVERS, CFG_OPT_CREATED)

        vers_new = vers
        build_new = str(int(build) + 1)
        created_new = dt.now().strftime('%Y-%m-%d')

        self.et_Version.SetValue(vers_new)
        self.st_VersionPrev.SetLabel(vers)
        self.et_Build.SetValue(build_new)
        self.st_BuildPrev.SetLabel(build)
        self.et_Created.SetValue(created_new)
        self.st_CreatedPrev.SetLabel(created)

        self.pc = []
        self.pc.append(re.compile(r'(.*# Version:\s*?)(\d+\.\d+\.\d+)', flags=re.MULTILINE | re.DOTALL))
        self.pc.append(re.compile(r'(.*# Build:\s*?)(\d+)', flags=re.MULTILINE | re.DOTALL))
        self.pc.append(re.compile(r'(.*# Created:\s*?)(\d{4}-\d{2}-\d{2})', flags=re.MULTILINE | re.DOTALL))
        return

    def save_vers(self):
        if self.pfname_vers is not None:
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_VERSION, self.et_Version.GetValue())
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_BUILD, self.et_Build.GetValue())
            self.ver_cfg.set(CFG_SEC_CURVERS, CFG_OPT_CREATED, self.et_Created.GetValue())
            with open(self.pfname_vers, 'w') as cf:
                self.ver_cfg.write(cf)
        return

    def ch_Directory_OnChoice(self, event):
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
        Set project directory

        :param event:
        :return:
        """
        with wx.DirDialog(None, "Choose Project Directory", self.path,
                          wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                value = dlg.GetPath()
                self.ch_Directory.Insert(value, 0)
                self.ch_Directory.SetSelection(0)
                self.read_vers(value)
        return

    def bt_Set_OnClick(self, event):
        """
        Save all values

        :param event:
        :return:
        """
        self.update_py_files([self.et_Version.GetValue(), self.et_Build.GetValue(), self.et_Created.GetValue()])
        return

    def bt_Revert_OnClick(self, event):
        """
        Restore previous values

        :param event:
        :return:
        """
        self.update_py_files(
            [self.st_VersionPrev.GetLabel(), self.st_BuildPrev.GetLabel(), self.st_CreatedPrev.GetLabel()])
        return

    def update_py_files(self, vals: list):
        """
        Replace values in all files

        :param vals: Values to replace
        :return:
        """
        for fn in self.pfnames_py:
            self.st_Status.SetLabel('Updating file {}'.format(fn))
            self.st_Status.Update()
            with open(fn, "r") as f:
                text = f.read()

                for i, v in enumerate(vals):
                    text = re.sub(self.pc[i], r'\g<1>' + v, text)

            with open(fn, "w") as f:
                f.write(text)

        self.st_Status.SetLabel('{} .py file(s) updated in {}'.format(len(self.pfnames_py), self.path))

        # Save new values to .ver file
        self.save_vers()
        return

    def bt_IncVersion_OnClick(self, event):
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

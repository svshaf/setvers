#!/usr/bin/env python3

#  ----------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:       Sergey Shafranskiy <sergey.shafranskiy@gmail.com>
#
# Version:      1.0.0
# Build:        27
# Created:      2018-12-01
#  ----------------------------------------------------------------------------

import wx
import re
import configparser as cp
from datetime import datetime as dt

import setvers_gui

import os

cfg_sec_curvers = 'Current Version'
cfg_opt_version = 'Version'
cfg_opt_build = 'Build'
cfg_opt_created = 'Created'


class MainFrame(setvers_gui.GUIFrame):

    def __init__(self, parent):
        """
        Class constructor
        """
        super(MainFrame, self).__init__(parent)

        self.read_vers(os.path.dirname(__file__))

    def read_vers(self, path):
        self.path = path
        self.SetTitle(self.path)
        self.fn_vers = os.path.join(self.path, '.vers')
        print(self.fn_vers)

        self.fpy = [os.path.abspath(os.path.join(self.path, fn)) for fn in os.listdir(self.path)
                    if os.path.isfile(os.path.join(self.path, fn)) and (os.path.splitext(fn)[1] == '.py')]
        print(self.fpy)

        self.st_Status.SetLabel('{} .py file(s) found in {}'.format(len(self.fpy), self.path))

        self.cfg = cp.ConfigParser()
        self.cfg.optionxform = str
        if not os.path.exists(self.fn_vers):
            self.cfg.add_section(cfg_sec_curvers)
            self.cfg.set(cfg_sec_curvers, cfg_opt_version, '1.0.0')
            self.cfg.set(cfg_sec_curvers, cfg_opt_build, '1')
            self.cfg.set(cfg_sec_curvers, cfg_opt_created, dt.now().strftime('%Y-%m-%d'))
            # cfg['Version History'] = {}

            with open(self.fn_vers, 'w') as cf:
                self.cfg.write(cf)
        else:
            self.cfg.read(self.fn_vers)

        vers = self.cfg.get(cfg_sec_curvers, cfg_opt_version)
        build = self.cfg.get(cfg_sec_curvers, cfg_opt_build)
        created = self.cfg.get(cfg_sec_curvers, cfg_opt_created)

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

    def bt_SelectDir_OnClick(self, event):
        """
        Set project directory

        :param event:
        :return:
        """
        with wx.DirDialog(None, "Choose project directory", self.path,
                          wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.read_vers(dlg.GetPath())
        return

    def bt_Set_OnClick(self, event):
        """
        Save all values

        :param event:
        :return:
        """
        self.write_all_files([self.et_Version.GetValue(), self.et_Build.GetValue(), self.et_Created.GetValue()])
        return

    def bt_Revert_OnClick(self, event):
        """
        Restore previous values

        :param event:
        :return:
        """
        self.write_all_files(
            [self.st_VersionPrev.GetLabel(), self.st_BuildPrev.GetLabel(), self.st_CreatedPrev.GetLabel()])
        return

    def write_all_files(self, vals: list):
        """
        Replace values in all files

        :param vals: Values to replace
        :return:
        """
        for fn in self.fpy:
            self.st_Status.SetLabel('Updating file {}'.format(fn))
            self.st_Status.Update()
            with open(fn, "r") as f:
                text = f.read()

                for i, v in enumerate(vals):
                    text = re.sub(self.pc[i], r'\g<1>' + v, text)

            with open(fn, "w") as f:
                f.write(text)

        self.st_Status.SetLabel('{} .py file(s) updated in {}'.format(len(self.fpy), self.path))

        # Save new values to .ver file
        self.cfg.set(cfg_sec_curvers, cfg_opt_version, self.et_Version.GetValue())
        self.cfg.set(cfg_sec_curvers, cfg_opt_build, self.et_Build.GetValue())
        self.cfg.set(cfg_sec_curvers, cfg_opt_created, self.et_Created.GetValue())
        with open(self.fn_vers, 'w') as cf:
            self.cfg.write(cf)
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

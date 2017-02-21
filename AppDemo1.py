# _*_ coding=utf-8 _*_

__author__ = 'Panda'

import wx


class FrameDemo(wx.Frame):
    def __int__(self, parent, title):
        wx.Frame.__init__(self, None, -1, "testframe！", (100, 100), (100, 100))


class MyApp(wx.App):
    def OnIntial(self):
        self.frame = FrameDemo()

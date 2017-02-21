#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import wx

__author__ = 'Huoyunren'


class SizerUsage(wx.Frame):
    def __init__(self, title):
        super(SizerUsage, self).__init__(None, id=wx.NewId(), title=title, pos=wx.DefaultPosition,
                                         size=(500, 600))
        self.panel1 = wx.Panel(self)
        self.panel1.SetBackgroundColour(wx.GREEN)
        self.CreateStatusBar()

        self.user_name_st = wx.StaticText(self.panel1, label=u"用户名:")
        self.pwd_st = wx.StaticText(self.panel1, label=u"密  码:")
        self.user_name_tc = wx.TextCtrl(self.panel1)
        self.pwd_tc = wx.TextCtrl(self.panel1, style=wx.PASSWORD)
        self.sure_bt = wx.Button(self.panel1, wx.ID_OK)

        self.mobile_st = wx.StaticText(self.panel1, label=u"手机号:")
        self.file_path_tc = wx.TextCtrl(self.panel1, size=(70, -1), style=wx.TE_MULTILINE)
        self.choice_bt = wx.Button(self.panel1, label=u"浏览...", size=(50, -1))

        self.Bind(wx.EVT_BUTTON, self.choice_mobile_file, self.choice_bt)

        # 布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        panel1_sizer = wx.BoxSizer(wx.VERTICAL)
        user_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pwd_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mobile_sizer = wx.BoxSizer(wx.HORIZONTAL)

        user_sizer.AddSpacer(50)
        user_sizer.Add(self.user_name_st)
        user_sizer.Add(self.user_name_tc)
        user_sizer.AddSpacer(50)

        pwd_sizer.AddSpacer(50)
        pwd_sizer.Add(self.pwd_st)
        pwd_sizer.Add(self.pwd_tc)
        pwd_sizer.AddSpacer(50)

        mobile_sizer.AddSpacer(20)
        mobile_sizer.Add(self.mobile_st)
        mobile_sizer.Add(self.file_path_tc)
        mobile_sizer.AddSpacer(10)
        mobile_sizer.Add(self.choice_bt)
        mobile_sizer.AddSpacer(10)

        panel1_sizer.AddSpacer(30)
        panel1_sizer.Add(user_sizer)
        panel1_sizer.AddSpacer(10)
        panel1_sizer.Add(pwd_sizer)
        panel1_sizer.Add(self.sure_bt, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)
        panel1_sizer.AddSpacer(30)
        panel1_sizer.Add(mobile_sizer)
        panel1_sizer.AddSpacer(30)
        self.panel1.SetSizer(panel1_sizer)

        sizer.Add(self.panel1, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize()

        self.Show(True)

    def choice_mobile_file(self, event):
        wild_card = u"所有Excel文件(*.xls,*.xlsx) | *.xls;*.xlsx"
        file_dlg = wx.FileDialog(self.panel1, message=u"选择文件", wildcard=wild_card, style=wx.FD_OPEN)
        if file_dlg.ShowModal() == wx.ID_OK:
            file_path = file_dlg.GetPath()
            msg = u"选中的文件路径为:" + file_path
            self.PushStatusText(msg)
            self.file_path_tc.SetValue(file_path)
        file_dlg.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    sizer_frame = SizerUsage(u"布局DEMO")
    app.MainLoop()

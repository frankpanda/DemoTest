#!/usr/bin/env python
# _*_ coding:utf-8 _*_

__author__ = 'xiong bing'

import wx
import os
# test


class SMSSender(wx.Frame):
    def __init__(self, title):
        super(SMSSender, self).__init__(None, id=wx.ID_ANY, title=title, size=(700, 540))
        self.mobile_file_path = None

        # 添加图标
        icon_path = os.path.abspath("./message.ico")
        frame_icon = wx.Icon(icon_path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(frame_icon)
        # 添加状态栏
        self.CreateStatusBar()

        self.panel_main = wx.Panel(self)

        # 添加各种控件
        self.file_st = wx.StaticText(self.panel_main, label=u"选择文件:", size=(30, -1))
        self.display_path_tc = wx.TextCtrl(self.panel_main, size=(70, -1))
        self.choice_bt = wx.Button(self.panel_main, label=u"浏览...", size=(30, -1))

        self.sms_st = wx.StaticText(self.panel_main, label=u"短信内容:", size=(30, -1))
        self.content_tc = wx.TextCtrl(self.panel_main, size=(200, 300), style=wx.TE_MULTILINE)
        self.reset_content_bt = wx.Button(self.panel_main, label=u"清空", size=(30, -1))
        self.send_bt = wx.Button(self.panel_main, label=u"发送", size=(30, -1))

        # 控件布局
        mobile_sizer = wx.BoxSizer(wx.HORIZONTAL)
        mobile_sizer.AddSpacer(30)
        mobile_sizer.Add(self.file_st)
        mobile_sizer.AddSpacer(10)
        mobile_sizer.Add(self.display_path_tc)
        mobile_sizer.AddSpacer(30)
        mobile_sizer.Add(self.choice_bt)

        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        content_sizer.AddSpacer(30)
        content_sizer.Add(self.sms_st)
        content_sizer.AddSpacer(10)
        content_sizer.Add(self.content_tc)

        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        control_sizer.Add(self.reset_content_bt, 0, wx.ALIGN_LEFT, 5)
        control_sizer.AddSpacer(30)
        control_sizer.Add(self.send_bt, 0, wx.ALIGN_LEFT, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.AddSpacer(20)
        main_sizer.Add(mobile_sizer)
        main_sizer.AddSpacer(10)
        main_sizer.Add(content_sizer)
        main_sizer.AddSpacer(10)
        main_sizer.Add(control_sizer)
        main_sizer.AddSpacer(20)
        self.panel_main.SetSizer(main_sizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel_main, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.SetInitialSize()

        # 事件绑定
        self.Bind(wx.EVT_BUTTON, self.click_choice_bt, self.choice_bt)
        self.Bind(wx.EVT_BUTTON, self.click_reset_bt, self.reset_content_bt)
        self.Bind(wx.EVT_BUTTON, self.click_send_bt, self.send_bt)

        self.Show(True)

    # 选中保存手机号的excel文件事件
    def click_choice_bt(self, event):
        wild_card = u"所有Excel文件(*.xls,*.xlsx) | *.xls;*.xlsx"
        file_dlg = wx.FileDialog(self.panel_main, message=u"选择文件", wildcard=wild_card, style=wx.FD_OPEN)
        if file_dlg.ShowModal() == wx.ID_OK:
            file_path = file_dlg.GetPath()
            self.display_path_tc.SetValue(file_path)
            # self.mobile_file_path = file_path
            print u"选中excel文件，文件路径为:" + file_path
        file_dlg.Destroy()

    # 清空短信内容事件
    def click_reset_bt(self, event):
        self.content_tc.SetValue("")
        print u"清空短信内容"

    # 发送短信事件
    def click_send_bt(self, event):
        current_num = 0
        excel_path = self.display_path_tc.GetValue().encode("utf-8")

        if excel_path == "":
            msg_dlg = wx.MessageDialog(self.panel_main, u"请选择保存手机号的Excel文件！")
            msg_dlg.ShowModal()
            msg_dlg.Destroy()

            return
    '''
        else:
            mobiles_num = PostParam.get_mobiles(excel_path)

        sender = PostParam()
        sms_content = self.content_tc.GetValue().encode("utf-8")
        if sms_content == "":
            msg_dlg = wx.MessageDialog(self.panel_main, u"短信内容不能为空！")
            msg_dlg.ShowModal()
            msg_dlg.Destroy()

            return
        for num in mobiles_num:
            current_num += 1
            status_msg = u"正在发送第%d个号码:%s" % (current_num, num)
            self.PushStatusText(status_msg)
            sender.send_sms(num, sms_content)

        self.PushStatusText(u"短信发送完成！")
        if sender.failed_num == 0:
            msg_info = u"所有短信发送成功！"
        else:
            msg_info = u"短信发送完成!成功发送%d条,失败%d条！\n" \
                       u"发送失败的手机号保存在D:\\send_failure_mobiles.txt文件中！" % (sender.success_num, sender.failed_num)
        msg_dlg = wx.MessageDialog(self.panel_main, msg_info)
        msg_dlg.ShowModal()
        msg_dlg.Destroy()
    '''

if __name__ == "__main__":
    app = wx.App(False)
    frame = SMSSender(u"短信发送器")
    app.MainLoop()

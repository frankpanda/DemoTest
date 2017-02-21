# _*_ coding=utf-8 _*_

__author__ = 'Panda'

import wx
import time


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(450, 500))
        self.panel = wx.Panel(self, size=(300, 400))
        self.panel.SetBackgroundColour(wx.GREEN)
        self.CreateStatusBar()

        # 创建菜单
        file_menu = wx.Menu()

        menu_about = file_menu.Append(wx.ID_ABOUT, "&About", "Information about this program!")
        file_menu.AppendSeparator()
        menu_exit = file_menu.Append(wx.ID_EXIT, "&Exit", "Exit this program!")

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)
        print("hello frame!")

        # CheckBoxes
        self.checkbox1 = wx.CheckBox(self.panel, label="2 state checkbox", pos=(20, 0))
        self.checkbox2 = wx.CheckBox(self.panel, label="3 state checkbox",
                                     style=wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER,
                                     pos=(20, 30))

        # text
        self.name_text = wx.StaticText(self.panel, label="username:", pos=(20, 50))
        self.name_ctrl = wx.TextCtrl(self.panel, pos=(80, 50))
        self.pwd_text = wx.StaticText(self.panel, label="password:", pos=(20, 80))
        self.pwd_ctrl = wx.TextCtrl(self.panel, style=wx.PASSWORD, pos=(80, 80))
        self.msg_button = wx.Button(self.panel, label=u"确定", pos=(60, 120))

        # 单选
        items = [u"苹果", u"香蕉", u"柿子"]
        self.choice = wx.Choice(self.panel, choices=items, pos=(20, 150))
        self.choice.SetSelection(1)

        # 绑定事件
        self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        # 绑定checkbox事件
        self.Bind(wx.EVT_CHECKBOX, self.on_check)
        self.Bind(wx.EVT_BUTTON, self.click_msg_button, self.msg_button)
        # 绑定单选
        self.Bind(wx.EVT_CHOICE, self.on_check, self.choice)

        self.Show(True)

    # 创建点击about事件
    def on_about(self, event):
        dlg = wx.MessageDialog(self, "about editor", "this is about information", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    # 创建退出程序事件
    def on_exit(self, event):
        self.Close(True)

    # 选中Checkbox的事件
    def on_check(self, event):
        e_obj = event.GetEventObject()
        if e_obj == self.checkbox1:
            checked = self.checkbox1.GetValue()
            msg = "Two State Clicked:%s" % checked
            self.PushStatusText(msg)
        elif e_obj == self.checkbox2:
            state = self.checkbox2.Get3StateValue()
            msg = "Three State Clicked:%d" % state
            self.PushStatusText(msg)
        else:
            event.Skip()

    # TextCtrl
    def click_msg_button(self, event):
        self.msg_button.Disable()
        time.sleep(2)
        msg_string = self.name_ctrl.GetValue() + ":" + self.pwd_ctrl.GetValue()
        if msg_string == ":":
            msg_string = u"请输入name和password!"
        msg_dlg = wx.MessageDialog(self, msg_string, u"信息", wx.OK)
        msg_dlg.ShowModal()
        msg_dlg.Destroy()

        self.msg_button.Enable()


    # 单选
    def on_choice(self, event):
        value = self.choice.GetStringSelection()
        index = self.choice.GetSelection()
        msg_dlg = wx.MessageDialog(self, "selected value is:%s;index is:%d" % (value, index), u"提示信息", wx.OK)
        msg_dlg.ShowModal()
        msg_dlg.Destroy()


app = wx.App(False)
frame = MyFrame(None, u"短信发送器")
app.MainLoop()
